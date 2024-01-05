from dao.JobDao import JobDao


class JobService():

    def getJobSalaryStatisticByJobType(self):
        jobDao = JobDao()
        try:
            rset = jobDao.getJobSalaryStatisticByJobType()
        finally:
            jobDao.close()
        return rset
        pass

    def getJobCountStatisticByJobType(self):
        jobDao = JobDao()
        try:
            rset = jobDao.getJobCountStatisticByJobType()
        finally:
            jobDao.close()
        return rset
        pass

    def getJobsPageList(self, search={}, page={'currentPage': 1, 'pageSize': 10}):
        jobDao = JobDao()
        try:
            rset = jobDao.getJobsPageList(search, page)
        finally:
            jobDao.close()
        return rset

        pass

    def getAllJobList(self):
        jobDao = JobDao()
        try:
            rset = jobDao.getAllJobsList()
        finally:
            jobDao.close()
        return rset
        pass

    def createJobsSimilar(self, params):
        jobDao = JobDao()
        try:
            rset = jobDao.createJobsSimilar(params)
        finally:
            jobDao.close()
        return rset
        pass
        # 根据职位ID和查询详情数据

    def getJobsByJobId(self, jobId):
        jobDao = JobDao()
        try:
            rset = jobDao.getJobsByJobId(jobId)
        finally:
            jobDao.close()
        return rset
        pass

    def getJobssimilarList(self, jobId):
        jobDao = JobDao()
        try:
            rset = jobDao.getJobssimilarList(jobId)
        finally:
            jobDao.close()
        return rset
        pass

    pass
