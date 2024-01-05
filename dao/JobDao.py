from dao.BaseDao import BaseDao


# 职位数据管理数据库操作类   DAO：database access object
class JobDao(BaseDao):

    # 添加职位信息
    def createJob(self, params=[]):
        sql = "insert into t_jobs (jobname,jobsalary, jobCompany, jobaddress,jobDetail, jobType,jobLowSalary, jobHighSalary, jobMeanSalary, jobCity) " \
              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # %s是占位符
        result = self.execute(sql, params)
        self.commit()
        return result
        pass

    # 基于职位类别统计职位平均薪资数据
    def getJobSalaryStatisticByJobType(self):
        sql = 'select avg(jobmeansalary) as meansalary, jobtype from t_jobs GROUP BY jobType '
        result = self.execute(sql)
        resultSet = self.fetchall()
        return resultSet
        pass

    # 基于职位类别统计职位数量
    def getJobCountStatisticByJobType(self):
        sql = 'select count(jobtype) as nums, jobtype from t_jobs group by jobtype '
        result = self.execute(sql)
        resultSet = self.fetchall()
        return resultSet
        pass

    # 分页查询职位列表数据
    def getJobsPageList(self, search={}, page={'currentPage': 1, 'pageSize': 10}):
        sql = "select jobId, jobName, jobSalary, jobCompany, jobAddress, jobType from t_jobs where 1=1 "
        params = []
        sql += " limit %s, %s "
        startRow = (page['currentPage'] - 1) * page['pageSize']
        params.append(startRow)
        params.append(page['pageSize'])
        result = self.execute(sql, params)
        rset = self.fetchall()
        return rset
        pass

    # 查询职位ID和详情数据
    def getAllJobsList(self):
        sql = "select jobId, jobName, jobDetail from t_jobs"
        result = self.execute(sql)
        rset = self.fetchall()
        return rset
        pass

    # 保存相似度分析结果数据
    def createJobsSimilar(self, params):
        sql = "insert into t_jobs_similar (jobId, similarJobId, cosSimilar) values (%s, %s, %s)"
        result = self.execute(sql, params)
        self.commit()
        return result
        pass

    # 根据职位ID和查询详情数据
    def getJobsByJobId(self, jobId):
        sql = "select jobId, jobName, jobDetail from t_jobs where jobid=%s "
        result = self.execute(sql, [jobId])
        rset = self.fetchone()
        return rset
        pass

    def getJobssimilarList(self, jobId):
        sql = "select jobId, jobName, jobSalary, jobCompany, jobAddress, jobType from t_jobs " \
              "where jobId in (select similarjobid from t_jobs_similar as ts where ts.jobid=%s) "
        params = [jobId]
        result = self.execute(sql, params)
        rset = self.fetchall()
        return rset
        pass

    # 根据职位名称查询全部信息
    def getJobByJobName(self, jobName):
        print(jobName)
        sql = "select * from t_jobs where jobName = %s"
        result = self.execute(sql, [jobName])
        print(result)
        rset = self.fetchone()
        return rset
        pass

    pass
