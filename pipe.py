from bitbucket_pipes_toolkit import Pipe
import re
import requests

variables = {
  'APP_PASS': {'type': 'string', 'required': True},
  'WORKSPACE': {'type': 'string', 'required': False},
  'REPO_SLUG': {'type': 'string', 'required': True},
  'BRANCH': {'type': 'string', 'required': True},
  'FILE_PATH': {'type': 'string', 'required': True},
  'NEW_TAG': {'type': 'string', 'required': False},
  'COMMIT_MESSAGE': {'type': 'string', 'required': False},
  'USERNAME': {'type': 'string', 'required': True},
  'BASE_URL': {'type': 'string', 'required': False, 'default': 'https://api.bitbucket.org'},
  'PROJECT_KEY': {'type': 'string', 'required': True},
  'IMAGE_NAME': {'type': 'list', 'required': True},
}

pipe = Pipe(schema=variables)

app_pass = pipe.get_variable('APP_PASS')
workspace = pipe.get_variable('WORKSPACE')
commit_msg = pipe.get_variable('COMMIT_MESSAGE')
baseurl = pipe.get_variable('BASE_URL')
projectKey = pipe.get_variable('PROJECT_KEY')
repoSlug = pipe.get_variable('REPO_SLUG')
filepath = pipe.get_variable('FILE_PATH')
username = pipe.get_variable('USERNAME')
image_name = pipe.get_variable('IMAGE_NAME')
new_tag = pipe.get_variable('NEW_TAG')
branch = pipe.get_variable('BRANCH')

pipe.log_info(app_pass)
pipe.log_info(workspace)
pipe.log_info(commit_msg)
pipe.log_info(baseurl)
pipe.log_info(projectKey)
pipe.log_info(filepath)
pipe.log_info(username)
pipe.log_info(image_name)
pipe.log_info(new_tag)
pipe.log_info(branch)


pipe.log_info("Executing the pipe...")

# Get file contents
response = requests.get(f'{baseurl}/2.0/repositories/{workspace}/{repoSlug}/src/{branch}/{filepath}', auth=(username, app_pass))
file_contents = response.content.decode()
pipe.log_info("File content fetched from bitbucket...")
pipe.log_info(file_contents)

for i in image_name:
  pattern = re.compile(fr"({i}:\s*)([\w.-]+)")
  updated_file = pattern.sub(fr"\g<1>{new_tag}", file_contents)
  file_contents = updated_file

pipe.log_info("Updated the File with new tag...")
pipe.log_info(updated_file)

files = {f'{filepath}': (updated_file)}
data = {
    'message': commit_msg,
    'branch': branch
}

print(data)

response = requests.post(
    f'{baseurl}/2.0/repositories/{workspace}/{repoSlug}/src/', 
    auth=(username, app_pass), files=files, data=data)


pipe.log_info("edited file on bitbucket with new commit...")
pipe.log_info(response)

pipe.success(message="Success!")