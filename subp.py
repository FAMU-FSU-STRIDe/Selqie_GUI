import subprocess

#only use shell argument with trusted/hardcoded input
#shell argument allows for running a command as a string
#subprocess.run('ls -la', shell = True)

#without shell for running multiple commands
#p1 = subprocess.run(['ls', '-la'], capture_output = True)

#decode puts the output back into a string to get the format we are looking for, without it is all jumbled and there is no spacing
#print(p1.stdout.decode())

#if dont want to use decode:
p1 = subprocess.run(['ls', '-la'], capture_output = True, text = True)
#print(p1.stdout)

#or
#p1 = subprocess.run(['ls', '-la'], stdout = subprocess.PIPE, text = True)
#print(p1.stdout)

command = ['mkdir', 'test']
target_dir = "/Users/maddyboss/Documents/4521"
#cwd allows to switch directories to run the command in
#result = subprocess.run(command, cwd = target_dir, capture_output=True, text=True)
#print(result.stdout)
p1 = subprocess.run(['ls'], cwd = target_dir, capture_output=True, text=True)
print(p1.stdout)