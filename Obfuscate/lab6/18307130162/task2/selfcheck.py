import hashlib

an_dirs = "task_answer.txt"
hash_dirs = "task_md5.txt"

with open(an_dirs, 'r') as fb, open(hash_dirs, 'r') as fc:
	lines = fb.readlines()
	lines = [i.strip().strip('\r') for i in lines]
	hashlines = fc.readlines()
	hashlines = [i.strip().strip('\r') for i in hashlines]
	i = 0
	for line in lines:
		m = hashlib.md5()
		b = line.encode(encoding='utf-8')
		m.update(b)
		hashline = m.hexdigest()
		if hashline == hashlines[i]:
			i+=1
			print("answer " + str(i) + " is correct")
		else:
			i+=1
			print("answer " + str(i) + " is wrong")