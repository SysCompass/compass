'''Module to update intalling progress by processing log file.'''
import logging
import os.path

from compass.db import database
from compass.db.model import LogProgressingHistory
from compass.log_analyzor.line_matcher import Progress
from compass.utils import setting_wrapper as setting


class FileFilter(object):
    """base class to filter log file."""
    def __str__(self):
        return self.__class__.__name__

    def filter(self, pathname):
        '''filter log file.

        Args:
            pathname: str, the absolute path name to the log file.

        Returns:
            None
        '''
        raise NotImplementedError(str(self))


class CompositeFileFilter(FileFilter):
    """filter log file based on the list of filters"""
    def __init__(self, filters):
        self.filters = filters

    def __str__(self):
        return 'CompositeFileFilter[%s]' % self.filters

    def appendFilter(self, file_filter):
        '''append filter.'''
        self.filters.append(file_filter)

    def filter(self, pathname):
        '''filter log file.'''
        for file_filter in self.filters:
            if not file_filter.filter(pathname):
                return False

        return True


class FilterFileExist(FileFilter):
    """filter log file if not exists."""
    def filter(self, pathname):
        '''filter log file.'''
        file_exist = os.path.isfile(pathname)
        if not file_exist:
            logging.error("%s is not exist", pathname)

        return file_exist


def getFileFilter():
    '''get file filter'''
    composite_filter = CompositeFileFilter([FilterFileExist()])
    return composite_filter


class FileReader(object):
    '''Class to read log file.

    The class provide support to read log file from the position
    it has read last time. and update the position when it finish
    reading the log.
    '''
    def __init__(self, pathname):
        self.pathname = pathname
        self.position = 0
        self.partial_line = ''

    def __str__(self):
        return (
            '%s[pathname:%s, position:%s, partial_line:%s]' % (
                self.__class__.__name__, self.pathname, self.position,
                self.partial_line
            )
        )

    def getHistory(self):
        '''Get log file read history from database.

        Args:
            None

        Returns:
            line_matcher_name: str, line matcher name.
            progress: Progress instance record the installing history.

        The function should be called out of database session.
        It reads the log_progressing_history table to get the
        position in the log file it has read in last run,
        the partial line of the log, the line matcher name
        in the last run, the progress, the message and the
        severity it has got in the last run.
        '''
        with database.session() as session:
            history = session.query(
                LogProgressingHistory).filter_by(
                pathname=self.pathname).first()
            if history:
                logging.log(logging.DEBUG - 1,
                            'get file %s history %s',
                            self.pathname, history)
                self.position = history.position
                self.partial_line = history.partial_line
                line_matcher_name = history.line_matcher_name
                progress = Progress(history.progress,
                                    history.message,
                                    history.severity)
            else:
                line_matcher_name = 'start'
                progress = Progress(0.0, '', None)

            return line_matcher_name, progress

    def updateHistory(self, line_matcher_name, progress):
        '''Update log_progressing_history table.

        Args:
            line_matcher_name: str, the line matcher name.
            progress: Progress instance to record the installing progress.

        Returns:
            None

        The function should be called out of database session.
        It updates the log_processing_history table.
        '''
        with database.session() as session:
            history = session.query(LogProgressingHistory).filter_by(
                pathname=self.pathname).first()

            if history:
                if history.position >= self.position:
                    logging.error(
                        '%s history position %s is ahead of currrent '
                        'position %s',
                        self.pathname,
                        history.position,
                        self.position)
                    return

                history.position = self.position
                history.partial_line = self.partial_line
                history.line_matcher_name = line_matcher_name
                history.progress = progress.progress
                history.message = progress.message
                history.severity = progress.severity
            else:
                history = LogProgressingHistory(
                    pathname=self.pathname, position=self.position,
                    partial_line=self.partial_line,
                    line_matcher_name=line_matcher_name,
                    progress=progress.progress,
                    message=progress.message,
                    severity=progress.severity)
                session.merge(history)
            logging.debug('update file %s to history %s',
                          self.pathname, history)

    def readline(self):
        '''log line generator.

        For the last line of the file, it may regenerate in the next line
        because there is no \n for the last line.
        '''
        try:
            with open(self.pathname) as logfile:
                old_position = self.position
                logfile.seek(self.position)
                while True:
                    line = logfile.readline()
                    self.partial_line += line
                    position = logfile.tell()
                    if position > self.position:
                        self.position = position

                    if self.partial_line.endswith('\n'):
                        yield_line = self.partial_line
                        self.partial_line = ''
                        yield yield_line
                    else:
                        logging.debug(
                            'did not read the whole line:\n%r\n'
                            'It means the end of the file reached.',
                            self.partial_line)
                        break

                if self.partial_line:
                    yield self.partial_line

                logging.debug('processing file %s log %s bytes',
                              self.pathname, self.position - old_position)

        except Exception as error:
            logging.error('failed to processing file %s', self.pathname)
            logging.exception(error)

        logging.debug('%s is read to %s', self.pathname, self.position)


class FileReaderFactory(object):
    '''factory class to create FileReader instance.'''

    def __init__(self, logdir, filefilter):
        self.logdir = logdir
        self.filefilter = filefilter

    def __str__(self):
        return '%s[logdir: %s filefilter: %s]' % (
            self.__class__.__name__, self.logdir, self.filefilter)

    def getFileReader(self, hostname, filename):
        '''Get FileReader instance.

        Args:
            hostname: str, the hostname of installing host.
            filename: the filename of the log file.

        Returns:
            FileReader instance if it is not filtered.
            Otherwise None.
        '''
        pathname = os.path.join(self.logdir, hostname, filename)
        logging.debug('Read %s', pathname)
        if not self.filefilter.filter(pathname):
            logging.error('%s is filtered', pathname)
            return None

        return FileReader(pathname)


FILE_READER_FACTORY = FileReaderFactory(
    setting.INSTALLATION_LOGDIR, getFileFilter())


class FileMatcher(object):
    '''
       File matcher the get the lastest installing progress
       from the log file.
    '''
    def __init__(self, line_matchers, min_progress, max_progress, filename):
        if not 0.0 <= min_progress <= max_progress <= 1.0:
            raise IndexError(
                '%s restriction is not mat: 0.0 <= min_progress'
                '(%s) <= max_progress(%s) <= 1.0' % (
                    self.__class__.__name__,
                    min_progress,
                    max_progress))

        self.line_matchers = line_matchers
        self.min_progress = min_progress
        self.max_progress = max_progress
        self.absolute_min_progress = 0.0
        self.absolute_max_progress = 1.0
        self.absolute_progress_diff = 1.0
        self.filename = filename

    def update_absolute_progress_range(self, min_progress, max_progress):
        '''update the min progress and max progress the log file indicates.'''
        progress_diff = max_progress - min_progress
        self.absolute_min_progress = (
            min_progress + self.min_progress * progress_diff)
        self.absolute_max_progress = (
            min_progress + self.max_progress * progress_diff)
        self.absolute_progress_diff = progress_diff

    def __str__(self):
        return (
            '%s[ filename: %s, progress range: [%s:%s], '
            'line_matchers: %s]' % (
                self.__class__.__name__, self.filename,
                self.absolute_min_progress,
                self.absolute_max_progress, self.line_matchers)
        )

    def updateTotalProgress(self, file_progress, total_progress):
        '''Get the total progress from file progress.

        Args:
            file_progress: Progress instance. the installing progress from
                           the logging file.
                           It is between 0 to 1. 1 means the whole log
                           installing progess for the related part is
                           done. it does not mean the whole installing
                           progress done.
            total_progrss: Progress instance. the total installing
                           progress to update.
                           It should be between absolute_min_progress
                           and absolute max progress.

        Returns:
            None
        '''
        if not file_progress.message:
            logging.info(
                'ignore update file %s progress %s to total progress',
                self.filename, file_progress)
            return

        total_progress_data = min(
            self.absolute_min_progress
                +
            file_progress.progress * self.absolute_progress_diff,
            self.absolute_max_progress)

        # total progress should only be updated when the new calculated
        # progress is greater than the recored total progress or the
        # progress to update is the same but the message is different.
        if (total_progress.progress < total_progress_data or
               (total_progress.progress == total_progress_data and
                   total_progress.message != file_progress.message)):
            total_progress.progress = total_progress_data
            total_progress.message = file_progress.message
            total_progress.severity = file_progress.severity
            logging.debug('update file %s total progress %s',
                          self.filename, total_progress)
        else:
            logging.info(
                'ignore update file %s progress %s to total progress %s',
                self.filename, file_progress, total_progress)  

    def updateProgress(self, hostname, total_progress):
        '''update progress from file.

        Args:
            hostname: str, the hostname of the installing host.
            total_progress: Progress instance to update.

        Returns:
            None

        the function update installing progress by reading the log file.
        It contains a list of line matcher, when one log line matches
        with current line matcher, the installing progress is updated.
        and the current line matcher got updated.
        Notes: some line may be processed multi times. The case is the
        last line of log file is processed in one run, while in the other
        run, it will be reprocessed at the beginning because there is
        no line end indicator for the last line of the file.
        '''
        file_reader = FILE_READER_FACTORY.getFileReader(hostname,
                                                        self.filename)
        if not file_reader:
            return

        line_matcher_name, file_progress = file_reader.getHistory()
        for line in file_reader.readline():
            if line_matcher_name not in self.line_matchers:
                logging.debug('early exit because %s is not in %s',
                              line_matcher_name, self.line_matchers)
                break

            index = line_matcher_name
            while index in self.line_matchers:
                line_matcher = self.line_matchers[index]
                index, line_matcher_name = line_matcher.updateProgress(
                    line, file_progress)

        file_reader.updateHistory(line_matcher_name, file_progress)
        self.updateTotalProgress(file_progress, total_progress)
