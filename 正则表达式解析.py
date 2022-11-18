class Tree:
	def __init__(self, root=None, left=None, right=None):
		self.root = root  # 数据域
		self.left = left  # 左子树
		self.right = right  # 右子树
def Bracket(s,i):
	Character=[]
	t=0#t用于计算该括号中的节点数量
	index=[-1,]#-1为哨兵
	while(i<len(s)):
		if (s[i]=='('):#读到左括号，进入下一层递归
			s, i, Character1 = Bracket(s, i+1)
			Character.extend(Character1)
			t+=1
		elif (s[i]==')'):
			index.append(len(Character)-1)
			if (t==1):
				return s,i+1,Character
			elif(len(index)!=2):
				while (len(index)!=1):
					j=index[len(index)-1]
					while (j>index[len(index)-2]+1):
						a = Character[j]
						b = Character[j - 1]
						del Character[j]
						c = Tree('+', b, a)
						Character[j - 1] = c
						j -= 1
						t -= 1
					index.pop()
				while(t>1):
					a = Character.pop()
					b = Character.pop()
					c = Tree('|', b, a)
					Character.append(c)
					t-=1
					return s, i + 1, Character
			else:
				while (t>1):
					a = Character.pop()
					b = Character.pop()
					c = Tree('+', b, a)
					Character.append(c)
					t -= 1
				return s,i+1,Character
		elif(s[i].isalpha()):
			c = Tree(s[i])
			Character.append(c)
			i += 1
			t+=1
		elif(s[i]=='*'):#'*'运算符优先级最高，直接连
			a=Character.pop()
			c=Tree('*',a)
			Character.append(c)
			i+=1
		else: #'|‘
			index.append(len(Character)-1)
			i+=1
def Translate(s,Character):
	index=[-1,]
	i=0
	while (i<len(s)):
		if (s[i].isalpha()):
			c=Tree(s[i])
			Character.append(c)
			i+=1
		elif (s[i]=='('):
			s,i,Character1=Bracket(s,i+1)
			Character.extend(Character1)
		elif (s[i]=='*'):
			a=Character.pop()
			c=Tree('*',a)
			Character.append(c)
			i+=1
		else: #'|'
			index.append(len(Character)-1)
			i+=1
	#处理剩余'|'
	index.append(len(Character)-1)
	while (len(index) != 1):
		j = index[len(index) - 1]
		while (j > index[len(index) - 2]+1):
			a = Character[j]
			b = Character[j-1]
			del Character[j]
			c = Tree('+', b, a)
			Character[j-1]=c
			j -= 1
		index.pop()
	while (len(Character)>1):
		a = Character.pop()
		b = Character.pop()
		c = Tree('|', b, a)
		Character.append(c)
def PrintTree(head,height,link,spacelen):
	if (head==None):
		return
	val=link+head.root
	PrintTree(head.right, height + 1, '/--', spacelen)
	lenM=len(val)
	lenL=int((spacelen-lenM)/2)
	lenR=spacelen - lenM - lenL
	val = " "*(lenL) + val + " "*(lenR)
	print(' '*(height*spacelen) + val)
	PrintTree(head.left, height + 1, '\\--',spacelen)
s=input()
Character = []
Translate(s,Character)
PrintTree(Character[0],0,"--",5)