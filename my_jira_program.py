import json
import subprocess
from datetime import datetime
from sys import exit

def getJiraObject(creds):
      try:
            userpass = tuple(list(creds.values())[:2])
            server_address = list(creds.values())[-1]
            return JIRA(server=server_address,
                        basic_auth=userpass)
      except:
            print "[!] Could not connect to Jira server"
            return None

def curlGetRequest(serverAddress, id):
      try:
            proc = subprocess.Popen(["curl",
            "--user", "mmalka@quadanalytix.com:svat9d0GBP16Rk4wRNUYA205",
            "--header", "Accept: application/json",
            "--url", "{0}/rest/api/2/issue/{1}/changelog".format(serverAddress, id)],
                  stdout=subprocess.PIPE)
            (out, err) = proc.communicate()
            if err: raise Exception
      except:
            print "[!] Error trying to run curl."
            print err
            print "exiting..."
            exit(1)
      return out

def printTimeDiff(data):
      assert data
      values = json.loads(data)['values']
      FMT = "%Y-%m-%dT%H:%M:%S.%f"
      ts_arr = []
      for val in values:
            _from = val['items'][0]['fromString']
            _to =  val['items'][0]['toString']
            _created = val['created']
            if val['items'][0]['fromString'] != None:
                  if (_from == "New" and _to == "In Progress") or (_from == "In Progress" and _to == "Code Review"):
                        ts_arr.append(datetime.strptime(_created[:-5], FMT))
      splitted_diff = str(ts_arr[1] - ts_arr[0]).split(".")[0].split(":")
      print "Writing DSL named {0} Took {1} : {2} Hours {3} Minutes and {4} Seconds".format(
            issue.key, 
            issue.fields.assignee,
            splitted_diff[0],
            splitted_diff[1],
            splitted_diff[2])


if __name__ == '__main__':
      ### TODO ###
      # (Optional) ask the user for a certain name and output only his tickets.
      # (Optional) ask for the range of ticket id's.
      try:
            from jira import JIRA
      except:
            print "[!] Could not load jira-python"
            print "[!] please install it ( pip install jira-python ) and restart the script"
      issue = None
      TICKET_PREFIX = "ALE-"
      my_creds = dict()
      with open('mycreds.txt', 'r') as _creds:
            my_creds = eval(_creds.readline())
      assert my_creds
      jira = getJiraObject(my_creds)
      assert jira
      for ticket_name in [TICKET_PREFIX+str(y) for y in [x for x in range(0,500)]]:
            try:
                  issue = jira.issue(ticket_name)
                  assert issue
                  data = curlGetRequest(my_creds['serverAddress'], issue.id)
                  printTimeDiff(data)
                  print '-'*100
            except:
                  print "[!] Ticket Named {0} Not Found!".format(ticket_name)
                  pass

# When a report would be needed:
# >>> arr = [["Moshe","ticket1","20 H"],["Limor","ticket202","3 H"],["Stas","ticket5","1.5 H"]]
# >>> arr
# [['Moshe', 'ticket1', '20 H'], ['Limor', 'ticket202', '3 H'], ['Stas', 'ticket5', '1.5 H']]
# >>> {v[0]:v[1:] for v in arr}
# {'Moshe': ['ticket1', '20 H'], 'Limor': ['ticket202', '3 H'], 'Stas': ['ticket5', '1.5 H']}
# >>>