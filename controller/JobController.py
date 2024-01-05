import json

import jieba
import numpy as np
from flask import request, render_template, Blueprint, redirect
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from service.JobService import JobService

jobController = Blueprint('jobController', __name__)
jobService = JobService()


# json接口，返回基于职位类型的json格式的薪资平均值统计数据
@jobController.route('/salarybytype', methods=['get', 'post'])
def jsonSalaryStatisticByJobType():
    data = jobService.getJobSalaryStatisticByJobType()
    return json.dumps(data, ensure_ascii=False)
    pass


@jobController.route('/countbytype', methods=['get', 'post'])
def jsonCountStatisticByJobType():
    data = jobService.getJobCountStatisticByJobType()
    return json.dumps(data, ensure_ascii=False)
    pass


@jobController.route('/jobslist', methods=['get', 'post'])
def jobsList():
    currentPage = request.form.get('currentPage')
    pageSize = request.form.get('pageSize')
    if currentPage and pageSize:
        currentPage = int(currentPage)
        pageSize = int(pageSize)
        pass
    else:
        currentPage = 1
        pageSize = 10
    page = {'currentPage': currentPage, 'pageSize': pageSize}
    search = {}

    pageList = jobService.getJobsPageList(search, page)
    return render_template('jobslist.html', search=search, page=page, pageList=pageList)
    pass


# 相似度分析实现
@jobController.route('/jobsimilar')
def jobSimilar():
    jobsList = jobService.getAllJobList()  # 查询全部的职位数据
    texts = []
    for job in jobsList:
        jobDetail = job.get('jobDetail')
        if jobDetail:
            jobDetail = jobDetail.replace('\n', '')
            texts.append(' '.join(jieba.cut(jobDetail)))
            # print(texts)
        pass
    # 构造词典，统计词频
    cv = CountVectorizer()
    tf = cv.fit_transform(texts)
    tfidfTransformer = TfidfTransformer()

    # 计算tf-idf
    tfiwf = tfidfTransformer.fit_transform(tf)
    # 查看每句话的tf-idf值
    print(tfiwf.toarray())

    from sklearn.metrics.pairwise import linear_kernel

    # 通过向量的余弦相似度，计算出第一个文本和所有其他文本之间的相似度（注意此处包含了自己）
    # 分析相似度最高的前10条职位数据
    for i, row in enumerate(tfiwf):
        cosine_similarities = linear_kernel(row, tfiwf).flatten()
        for j in range(11):
            index = np.argmax(cosine_similarities)
            jobs = jobsList[index]
            currentJobs = jobsList[i]
            if jobs['jobId'] != currentJobs['jobId']:
                # 插入数据库
                params = [currentJobs['jobId'], jobs['jobId'], cosine_similarities[index]]
                result = jobService.createJobsSimilar(params)
                if result > 0:
                    print("添加成功")
                    pass
                pass
            cosine_similarities[index] = 0  # 每次找到相似度最高的后，将相似度置为0,
    return redirect('/jobslist')
    pass


@jobController.route('/jobdetail')
def jobDetail():
    jobId = request.args.get('jobid')
    jobs = jobService.getJobsByJobId(jobId)
    pageList = jobService.getJobssimilarList(jobId)
    return render_template('jobdetails.html', jobs=jobs, pageList=pageList)
    pass
