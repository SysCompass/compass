'''
   Module about line matcher to get the progress when found match 
   with a line of the log.
'''
import logging
import re

from compass.utils import util


class Progress(object):
    '''Progress object to store installing progress and message.'''

    def __init__(self, progress, message, severity):
        self.progress = progress
        self.message = message
        self.severity = severity

    def __str__(self):
        return '%s[progress:%s, message:%s, severity:%s]' % (
            self.__class__.__name__,
            self.progress,
            self.message,
            self.severity)


class ProgressCalculator(object):
    """base class to generate progress."""
    def __init__(self):
        raise NotImplementedError(str(self))

    @classmethod
    def updateProgress(cls, progress_data, message,
                       severity, progress):
        '''
            Update progress with the given progress_data,
            message and severity.

        Args:
            progress_data: float between 0 to 1.
            message: str, installing progress message.
            severity: installing message severity.
                      Should be in one of 
                      ['ERROR', 'WARNING', 'INFO'].
                      'ERROR' means there is some errors
                      in installing.

            progress: Progress instance to update.

        Returns:
            None
        '''
        # the progress is only updated when the new progress
        # is greater than the stored progress or the progress
        # to update is the same but the message is different.
        if (progress_data > progress.progress or
               (progress_data == progress.progress and
                   message != progress.message)):
            progress.progress = progress_data
            if message:
                progress.message = message

            if severity:
                progress.severity = severity

            logging.debug('update progress to %s', progress)
        else:
            logging.info('ignore update progress %s to %s',
                         progress_data, progress)

    def update(self, message, severity, progress):
        '''interface to update progress by message and severity.

        Args:
            message: str, installing message.
            severity: str, installing severity.

        Returns:
            None
        '''
        raise NotImplementedError(str(self))

    def __str__(self):
        return self.__class__.__name__


class IncrementalProgress(ProgressCalculator):
    '''Class to increment the progress.'''
    def __init__(self, min_progress,
                 max_progress, incremental_ratio):
        if not 0.0 <= min_progress <= max_progress <= 1.0:
            raise IndexError(
                '%s restriction is not mat: 0.0 <= min_progress(%s)'
                ' <= max_progress(%s) <= 1.0' % (
                    self.__class__.__name__, min_progress, max_progress))

        if not 0.0 <= incremental_ratio <=  1.0:
            raise IndexError(
                '%s restriction is not mat: '
                '0.0 <= incremental_ratio(%s) <=  1.0' % (
                    self.__class__.__name__, incremental_ratio))

        self.min_progress = min_progress
        self.max_progress = max_progress
        self.incremental_progress = (
            incremental_ratio * (max_progress - min_progress))

    def __str__(self):
        return '%s[%s:%s:%s]' % (
            self.__class__.__name__,
            self.min_progress,
            self.max_progress,
            self.incremental_progress
        )

    def update(self, message, severity, progress):
        '''update progress from message and severity.'''
        progress_data = max(
            self.min_progress,
            min(
                self.max_progress,
                progress.progress + self.incremental_progress
            )
        )
        self.updateProgress(progress_data,
                            message, severity, progress)


class RelativeProgress(ProgressCalculator):
    '''class to update progress to the given relative progress.'''
    def __init__(self, progress):
        if not 0.0 <= progress <= 1.0:
            raise IndexError(
                '%s restriction is not mat: 0.0 <= progress(%s) <= 1.0' % (
                    self.__class__.__name__, progress))
        self.progress = progress

    def __str__(self):
        return '%s[%s]' % (self.__class__.__name__, self.progress)

    def update(self, message, severity, progress):
        'update progress from message and severity.'''
        self.updateProgress(
            self.progress, message, severity, progress)


class SameProgress(ProgressCalculator):
    '''class to update message and severity for  progress.'''
    def update(self, message, severity, progress):
        '''update progress from the message and severity.'''
        self.updateProgress(progress.progress, message,
                            severity, progress)


class LineMatcher(object):
    '''Progress matcher for each line.'''

    def __init__(self, pattern, progress=None,
                 message_template='', severity=None,
                 unmatch_sameline_next_matcher_name='',
                 unmatch_nextline_next_matcher_name='',
                 match_sameline_next_matcher_name='',
                 match_nextline_next_matcher_name=''):
        self.regex = re.compile(pattern)
        if not progress:
            self.progress = SameProgress()
        elif isinstance(progress, ProgressCalculator):
            self.progress = progress
        elif util.isInstanceOf(progress, [int, float]):
            self.progress = RelativeProgress(progress)
        else:
            raise TypeError(
                'progress unsupport type %s: %s' % (
                    type(progress), progress))

        self.message_template = message_template
        self.severity = severity
        self.unmatch_sameline_next_matcher_name = \
            unmatch_sameline_next_matcher_name
        self.unmatch_nextline_next_matcher_name = \
            unmatch_nextline_next_matcher_name
        self.match_sameline_next_matcher_name = \
            match_sameline_next_matcher_name
        self.match_nextline_next_matcher_name = \
            match_nextline_next_matcher_name

    def __str__(self):
        return '%s[pattern:%r, message_template:%r, severity:%r]' % (
            self.__class__.__name__, self.regex.pattern,
            self.message_template, self.severity)

    def updateProgress(self, line, progress):
        '''update progress by the line.

        Args:
            line: str, one line in log file to indicate the
                  installing progress. The line may be partial
                  if the latest line of the log file is not the
                  whole line. But the whole line may be resent
                  in the next run.
            progress: the Progress instance to update.

        Returns:
            None
        '''
        mat = self.regex.search(line)
        if not mat:
            return (
                self.unmatch_sameline_next_matcher_name,
                self.unmatch_nextline_next_matcher_name)

        self.progress.update(self.message_template % mat.groupdict(),
                             self.severity, progress)
        logging.debug('line match\n%s\n'
                      'the matcher for the same line is %s '
                      'and for the next line is %s',
                      line, self.match_sameline_next_matcher_name,
                      self.match_nextline_next_matcher_name)
        return (
            self.match_sameline_next_matcher_name,
            self.match_nextline_next_matcher_name)
