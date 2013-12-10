'''Module to provider installing progress update functions for the adapter.'''
import logging
import re

from compass.db import database
from compass.db.model import Cluster, ClusterHost
from compass.log_analyzor.line_matcher import Progress


class AdapterItemMatcher(object):
    '''
       progress matcher for the os installing or package installing.
    '''
    def __init__(self, file_matchers):
        self.file_matchers = file_matchers
        self.min_progress = 0.0
        self.max_progress = 1.0

    def update_progress_range(self, min_progress, max_progress):
        '''update min_progress and max_progress.'''
        self.min_progress = min_progress
        self.max_progress = max_progress
        for file_matcher in self.file_matchers:
            file_matcher.update_absolute_progress_range(
                self.min_progress, self.max_progress)

    def __str__(self):
        return '%s[file_matchers: %s, min_progress: %s, max_progress: %s]' % (
            self.__class__.__name__, self.file_matchers,
            self.min_progress, self.max_progress)

    def updateProgress(self, hostname, progress):
        '''Update progress.

        Args:
            hostname: str, the hostname of the installing host.
            progress: Progress instance to update.

        Returns:
            None
        '''
        for file_matcher in self.file_matchers:
            file_matcher.updateProgress(hostname, progress)


class AdapterMatcher(object):
    '''Adapter matcher to update adapter installing progress.'''

    # TODO(weidong): arg list too long
    def __init__(self, name, os_pattern, os_matcher,
                 min_os_progress, max_os_progress,
                 package_installer_name, package_matcher,
                 min_package_progress, max_package_progress):
        if not (0.0 <= min_os_progress <= max_os_progress  <=
                   min_package_progress <= max_package_progress <= 1.0):
            raise IndexError('%s restriction is not met: '
                             '0.0 <= min_os_progress(%s) <='
                             ' max_os_progress(%s) <= min_package_progress(%s)'
                             ' <= max_package_progress(%s)' % (
                                 name, min_os_progress, max_os_progress,
                                 min_package_progress, max_package_progress))

        self.name = name
        self.os_regex = re.compile(os_pattern)
        self.os_matcher = os_matcher
        self.os_matcher.update_progress_range(
            min_os_progress, max_os_progress)
        self.package_installer_name = package_installer_name
        self.package_matcher = package_matcher
        self.package_matcher.update_progress_range(
            min_package_progress, max_package_progress)

    def match(self, os_name, package_installer_name):
        '''
           Check if the adapter matcher is acceptable for the given 
           os name and package installer.

        Args:
            os_name: str, the os name.
            package_installer_name: str, the package installer name.

        Returns:
            True if found the AdapterMatcher can process the log files
            generated for the os installation and package installation.
        '''
        if (self.os_regex.match(os_name) and
               self.package_installer_name == package_installer_name):
            return True

        return False

    def __str__(self):
        return '%s[name:%s, os_matcher:%s, package_matcher:%s]' % (
            self.__class__.__name__, self.name,
            self.os_matcher, self.package_matcher)

    @classmethod
    def getHostProgress(cls, hostid):
        '''Get Host Progress from database.

        Args:
            hostid: int, the id of host in database.

        Returns:
            Progress instance got from database or None if there is
            no such record.

        Notes: The function should be called out of database session. 
        '''
        with database.session() as session:
            host = session.query(
                ClusterHost).filter_by(
                id=hostid).first()
            if not host:
                logging.error(
                    'there is no host for %s in ClusterHost', hostid)
                return None, None, None

            if not host.state:
                logging.error('there is no related HostState for %s',
                              hostid)
                return host.hostname, None, None

            return (
                host.hostname,
                host.state.state,
                Progress(host.state.progress,
                         host.state.message,
                         host.state.severity))

    @classmethod
    def updateHostProgress(cls, hostid, progress):
        '''update host progress to database.

        Args:
            hostid: int, the id of the ClusterHost in database.
            progress: Progress instance to update.

        Returns:
            None

        the progress will be updated to database if the value is greater than
        the progress in the database or the value is the same but the message
        is different.

        Notes: the function should be called out of the database session.
        '''
        with database.session() as session:        
            host = session.query(
                ClusterHost).filter_by(id=hostid).first()
            if not host:
                logging.error(
                    'there is no host for %s in ClusterHost', hostid)
                return

            if not host.state:
                logging.error(
                    'there is no related HostState for %s', hostid)
                return

            if host.state.state != 'INSTALLING':
                logging.error(
                    'host %s is not in INSTALLING state',
                    hostid)
                return

            if host.state.progress > progress.progress:
                logging.error(
                    'host %s progress is not increased '
                    'from %s to %s',
                    hostid, host.state, progress)
                return

            if (host.state.progress == progress.progress and
                host.state.message == progress.message):
                logging.info(
                    'ignore update host %s progress %s to %s',
                    hostid, progress, host.state)
                return

            if progress.progress >= 1.0:
                host.state.state = 'READY'
            
            host.state.progress = progress.progress
            host.state.message = progress.message

            if progress.severity:
                host.state.severity = progress.severity

            if progress.severity == 'ERROR':
                host.state.state = 'ERROR'
                logging.debug(
                    'update host %s state %s',
                    hostid, host.state)

    @classmethod
    def getClusterProgress(cls, clusterid):
        '''Get cluster progress from database.

        Args:
            clusterid: int, cluster id for the cluster.

        Returns:
            Progress instance from database.

        Notes: the function should be called out of database session.
        '''
        with database.session() as session:
            cluster = session.query(Cluster).filter_by(id=clusterid).first()
            if not cluster:
                logging.error('there is no Cluster for %s', clusterid)
                return None, None

            if not cluster.state:
                logging.error('there is no ClusterState for %s', clusterid)
                return None, None

            return (
                cluster.state.state,
                Progress(cluster.state.progress,
                         cluster.state.message,
                         cluster.state.severity))

    @classmethod
    def updateClusterProgress(cls, clusterid, progress):
        '''update cluster installing progress to database.

        Args:
            clusterid: int, cluster id.
            progress: Progress instance to update to database.

        Returns:
            None

        the progress will be updated to database if the value is greater than
        the progress in the database or the value is the same but the message
        is different.

        Notes: the function should be called out of the database session.
        '''
        with database.session() as session:
            cluster = session.query(
                Cluster).filter_by(id=clusterid).first()
            if not cluster:
                logging.error(
                    'there is no cluster for %s in Cluster',
                    clusterid)
                return

            if not cluster.state:
                logging.error(
                    'there is no ClusterState for %s',
                    clusterid)

            if cluster.state.state != 'INSTALLING':
                logging.error('cluster %s is not in INSTALLING state',
                              clusterid)
                return

            if cluster.state.progress > progress.progress:
                logging.error(
                    'cluster %s progress is not increased from %s to %s',
                    clusterid, cluster.state, progress)
                return

            if (cluster.state.progress == progress.progress and
                cluster.state.message == progress.message):
                logging.info(
                    'ignore update cluster  %s progress %s to %s',
                    clusterid, progress, cluster.state)
                return
                            
            if progress.progress >= 1.0:
                cluster.state.state = 'READY'

            cluster.state.progress = progress.progress
            cluster.state.message = progress.message

            if progress.severity:
                cluster.state.severity = progress.severity
            
            if progress.severity == 'ERROR':
                cluster.state.state = 'ERROR'

            logging.debug(
                'update cluster %s state %s',
                clusterid, cluster.state)

    def updateProgress(self, clusterid, hostids):
        '''update cluster progress and hosts progresses.

        Args:
            clusterid: int, the cluster id.
            hostids: list of int, the host ids.

        Returns:
            None
        '''
        cluster_state, cluster_progress = self.getClusterProgress(clusterid)
        if not cluster_progress:
            logging.error(
                'nothing to update cluster %s => state %s progress %s',
                clusterid, cluster_state, cluster_progress)
            return

        logging.debug('got cluster %s state %s progress %s',
                      clusterid, cluster_state, cluster_progress)
        host_progresses = {}
        for hostid in hostids:
            hostname, host_state, host_progress = self.getHostProgress(hostid)
            if not hostname or not host_progress:
                logging.error(
                    'nothing to update host %s => hostname %s '
                    'state %s progress %s',
                    hostid, hostname, host_state, host_progress)  
                continue

            logging.debug('got host %s hostname %s state %s progress %s',
                          hostid, hostname, host_state, host_progress)
            host_progresses[hostid] = (hostname, host_state, host_progress)

        for hostid, host_value in host_progresses.items():
            hostname, host_state, host_progress = host_value
            if host_state == 'INSTALLING' and host_progress.progress < 1.0:
                self.os_matcher.updateProgress(
                    hostname, host_progress)
                self.package_matcher.updateProgress(
                    hostname, host_progress)
                self.updateHostProgress(hostid, host_progress)
            else:
                logging.error(
                    'there is no need to update host %s '
                    'progress: hostname %s state %s progress %s',
                    hostid, hostname, host_state, host_progress)

        cluster_progress_data = 0.0
        for _, _, host_progress in host_progresses.values():
            cluster_progress_data += host_progress.progress

        cluster_progress.progress = cluster_progress_data / len(hostids)
        messages = []
        for _, _, host_progress in host_progresses.values():
            if host_progress.message:
                messages.append(host_progress.message)

        if messages:
            cluster_progress.message = '\n'.join(messages)

        for severity in ['ERROR', 'WARNING', 'INFO']:
            cluster_severity = None
            for _, _, host_progress in host_progresses.values():
                if host_progress.severity == severity:
                    cluster_severity = severity
                    break

            if cluster_severity:
                cluster_progress.severity = cluster_severity
                break

        self.updateClusterProgress(clusterid, cluster_progress)
