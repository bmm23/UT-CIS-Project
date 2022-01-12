from os import link, write
import requests
from bs4 import BeautifulSoup
import json
import io
import re
import time
import requests
import os.path

cookies = {
    'csrftoken-studentfinancials.mytuitionbill-Prod':
    '6kiZx7OERXh7GFHH9iUM0L9xvHiyYj9qKrJOgkOGVpZ4ZGZ3l5JuzhI93not7nXw',
    'ut_persist':
    '1862707392.47873.0000',
    '_shibsession_64656661756c7468747470733a2f2f75746469726563742e7574657861732e6564752f73686962626f6c657468':
    '_6f947ee22ffa709b5e0ed972454f8656',
    'SC':
    'AQEBBwID6gIQRjg0MDZENTA4QjIxNDRBMgYkVkZMRjExS0YxZkZJSTFuMzF4VU8zeG1HZllVdnRLNVpsMW5CBAoxNjQyMDE2OTAyBQ8yMDkuMTY2LjEyMi4xOTcDB2JtbTM4ODYKAVkIgLKUtu9NpMs7BWV6ZRAGwxYCdJDg+fT7JlxLdjTWT4bOWj/if4867FVaCtxoOAAWRWhTp7+saOhouUJdkQ3x9ow9lk3oYvDc1ZCABMxonnxB7rFhaalw3F0V6vnSKh1BsFqnu46pJNP72wKG4cQYshQMeNFDBsIMi9aKLbvognxE',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua':
    '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer':
    'https://utdirect.utexas.edu/ctl/ecis/results/view_results.WBX?s_me_cis_id=2012232265000001',
    'Accept-Language': 'en-US,en;q=0.9',
    'If-Modified-Since': 'Tue, 11 Jan 2022 15:33:19 CST',
}

params = (('s_me_cis_id', '2012232265000001'), )

response = requests.get(
    'https://utdirect.utexas.edu/ctl/ecis/results/view_results.WBX',
    headers=headers,
    params=params,
    cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://utdirect.utexas.edu/ctl/ecis/results/view_results.WBX?s_me_cis_id=2012232265000001', headers=headers, cookies=cookies)
#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://utdirect.utexas.edu/ctl/ecis/results/view_results.WBX?s_me_cis_id=2011241555000001', headers=headers, cookies=cookies)


def pythonScraper(link):
    save_path = 'C:/Users/Brendan/Desktop/scraper extension/reportjsons'

    def spaceRemover(string):
        return ' '.join(string.split())

    uniqueID = ''.join(re.findall(r'\d+', link))

    try:
        response = requests.get(link, headers=headers, cookies=cookies)
    except:
        print('cookie timed out')

    soup = BeautifulSoup(response.content, 'html.parser')

    def reportScrape(link):
        try:
            response = requests.get(link, headers=headers, cookies=cookies)
        except:
            return ('cookie timed out, refresh')

        soup = BeautifulSoup(response.content, 'html.parser')

        fieldSet = soup.find('fieldset')
        detailsList = [div.contents[1] for div in fieldSet.find_all('div')]

        instructorName = spaceRemover(detailsList[0])
        courseID = spaceRemover(detailsList[1])
        organization = spaceRemover(detailsList[2])
        college = spaceRemover(detailsList[3])
        semester = spaceRemover(detailsList[4])
        enrolledStudents = spaceRemover(detailsList[5])
        formsReturned = spaceRemover(fieldSet.find_all('div')[-1].contents[2])

        tableZeroAnswers = {
            'Instructor': instructorName,
            'Course ID': courseID,
            'Organization': organization,
            'College/School': college,
            'Semester': semester,
            'Grade-eligible enrollment': enrolledStudents,
            'Number of survey forms returns': formsReturned
        }

        tableOne = soup.find_all('table')[0]
        tableOneAnswers = {}
        tableOneKey = [
            'Strongly Disagree', 'Disagree', 'Neutral', 'Agree',
            'Strongly Agree', 'Number of Respondents', 'Average',
            'Organization Average', 'College/School Average',
            'University Average'
        ]

        tableOneAnswers['The course was well organized.'] = dict(
            zip(tableOneKey, [
                td.string.split(' ')[0] for td in tableOne.find_all('td')[1:11]
            ]))
        tableOneAnswers[
            'The instructor communicated information effectively.'] = dict(
                zip(tableOneKey, [
                    td.string.split(' ')[0]
                    for td in tableOne.find_all('td')[12:22]
                ]))
        tableOneAnswers[
            'The instructor showed interest in the progress of students.'] = dict(
                zip(tableOneKey, [
                    td.string.split(' ')[0]
                    for td in tableOne.find_all('td')[23:33]
                ]))
        tableOneAnswers[
            'The tests/assignments were usually graded and returned promptly.'] = dict(
                zip(tableOneKey, [
                    td.string.split(' ')[0]
                    for td in tableOne.find_all('td')[34:44]
                ]))
        tableOneAnswers[
            'The instructor made me feel free to ask questions, disagree, and express my ideas.'] = dict(
                zip(tableOneKey, [
                    td.string.split(' ')[0]
                    for td in tableOne.find_all('td')[45:55]
                ]))
        tableOneAnswers[
            'At this point in time, I feel that this course will be (or has already been) of value to me.'] = dict(
                zip(tableOneKey, [
                    td.string.split(' ')[0]
                    for td in tableOne.find_all('td')[56:66]
                ]))

        tableTwo = soup.find_all('table')[1]
        tableTwoAnswers = {}
        tableTwoKey = [
            'Very Unsatisfactory', 'Unsatisfactory', 'Satisfactory',
            'Very Good', 'Excellent', 'Number of respondents', 'Average',
            'Organization Average', 'College/School Average',
            'University Average'
        ]

        tableTwoAnswers['Overall, this instructor was'] = dict(
            zip(tableTwoKey, [
                td.string.split(' ')[0] for td in tableTwo.find_all('td')[1:11]
            ]))
        tableTwoAnswers['Overall, this course was'] = dict(
            zip(tableTwoKey, [
                td.string.split(' ')[0]
                for td in tableTwo.find_all('td')[12:22]
            ]))

        tableThree = soup.find_all('table')[2]
        tableThreeAnswers = {}
        tableThreeKey = [
            'Excessive', 'High', 'Average', 'Light', 'Insufficient',
            'Number of respondents', 'Average', 'Organization Average',
            'College/School Average', 'University Average'
        ]

        tableThreeAnswers[
            'In my opinion, the workload in this course was'] = dict(
                zip(tableThreeKey, [
                    td.string.split(' ')[0]
                    for td in tableThree.find_all('td')[1:11]
                ]))

        finalAnswers = [
            tableZeroAnswers, tableOneAnswers, tableTwoAnswers,
            tableThreeAnswers
        ]

        return finalAnswers

    def exportData(data):
        try:
            to_unicode = unicode
        except NameError:
            to_unicode = str
        data = reportScrape(link)

        with io.open(os.path.join(save_path, '{}.json'.format(uniqueID)),
                     'w',
                     encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
            outfile.write(to_unicode(str_))

    exportData(reportScrape(link))
    time.sleep(0.5)


def writeStop():
    with open('stoppplace.txt', 'r') as f:
        lastPlace = int(f.read())
    with open('stoppplace.txt', 'w') as f:
        f.write(str(lastPlace + 1))


def currentPos():
    with open('stoppplace.txt', 'r') as f:
        lastPlace = int(f.read())
    return lastPlace


def do1000():
    dataJson = json.load(open('data.json'))
    files = dataJson[(currentPos() * 1000):((currentPos() + 1) * 1000)]
    for link in files:
        pythonScraper(link)
        print('working')
    writeStop()


do1000()