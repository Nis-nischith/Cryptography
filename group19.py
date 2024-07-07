import datetime 
import hmac
import secrets
import datetime
import hashlib
import random

class createBlock:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8')+
                   str(self.nonce).encode('utf-8'))
        return sha.hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return createBlock(0, datetime.datetime.now(), "Entry block - NO DATA STORED", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)


class Miner:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def mineBlock(self, data):
        latest_block = self.blockchain.get_latest_block()
        new_block = createBlock(latest_block.index + 1, datetime.datetime.now(), data, latest_block.hash)
        proof = self.proof_of_work(new_block)
        new_block.hash = proof[0]
        new_block.nonce = proof[1]
        self.blockchain.add_block(new_block)
        print("\ncreateBlock mined successfully!")
        print("\nTimestamp:", new_block.timestamp, "Index:", new_block.index)
        print("\n",data,"\n")

    def proof_of_work(self, block):
        target = "0000"  # Set the target difficulty
        while True:
            hash = block.calculate_hash() 
            if hash[:len(target)] == target:
                return (hash, block.nonce)   
            block.nonce += 1

# course_id is 5 digit number like 11068 

class Course: 
    def __init__(self,course_id, course_name, sid,student_name,eid, edu_name,secret_key ):
        self.sid= sid
        self.student_name= student_name
        self.course_id=course_id
        self.course_name=course_name
        self.eid= eid
        self.edu_name = edu_name
        self.secret_key = secret_key

class Student:
    def __init__(self, student_name, sid):
        self.sid= sid
        self.student_name = student_name
        self.course_list = []
        
    def add_course(self, course_id, course_name, eid, edu_name):
        secret_key= random.randint(0, 2**10) + course_id
        self.course_list.append(Course(course_id, course_name, self.sid,self.student_name,eid, edu_name,secret_key))
        return secret_key
 

class Educator:
    def __init__(self, educator_name, eid):
        self.eid= eid
        self.educator_name = educator_name
        self.course_list = []
        
    def add_course(self, course_id, course_name, sid, student_name, student_key):
        self.course_list.append(Course(course_id, course_name, sid, student_name,self.eid,self.educator_name,student_key))
   
class verifyTransaction:

    def generate_bit(self):
        """Generate a random bit (0 or 1)."""
        return secrets.randbelow(2)

    def create_response(self, challenge, bit):
        """Create HMAC response using challenge and secret key."""
        # Combine challenge and bit
        combined_data = challenge + bytes([bit])
        return combined_data

    
    def get_hmac(self, data, user, transaction):
        course_key = 0;
        for course in user.course_list:
            if(course.course_id == transaction['course_id']):
                course_key = course.secret_key
        course_key= course_key.to_bytes(16, byteorder='big')
        return hmac.new(course_key, data, hashlib.sha256).digest()

    def verify_transaction(self, transaction, student, educator):
        user_id = transaction['user_id']
        amount = transaction['amount']
        response=self.create_response(transaction['challenge'],self.generate_bit())
        received_hmac = self.get_hmac(response,student,transaction)
        expected_hmac = 0
        for i in range(len(educator.course_list)):
            if (educator.course_list[i].course_id==transaction['course_id'] and educator.course_list[i].sid==student.sid):
                x= educator.course_list[i].secret_key.to_bytes(16, byteorder='big')
                expected_hmac = hmac.new(x,response, hashlib.sha256).digest()

        # Compare the received HMAC with the expected HMAC
        hmac_verified = hmac.compare_digest(expected_hmac, received_hmac)
        return hmac_verified


# Example usage:

blockchain = Blockchain()
miner= Miner(blockchain)

transactions=[]
users=[]
educator=[]
transaction_count=0

Alice = Student('Alice',45 )
key= Alice.add_course(11068, 'Blockchain', 678, 'Bob')
Bob = Educator('Bob', 678)
Bob.add_course(11068, 'Blockchain', 45, 'Alice', key)
key = Alice.add_course(11065, 'ML', 678, 'Bob')
Bob.add_course(11065, 'ML', 45, 'Alice', key)
Nis = Student('Nis',30 )
key= Nis.add_course(11068, 'Blockchain', 678, 'Bob')
Bob.add_course(11068, 'Blockchain', 30, 'Nis', key)
key= Nis.add_course(11065, 'ML', 420, 'Chits')
Chits= Educator('Chits', 420)
Chits.add_course(11065, 'ML', 30, 'Nis', key)
key = Alice.add_course(11069, 'Crypto', 420, 'Chits')
Chits.add_course(11069, 'Crypto', 45, 'Alice', key)
users.append(Nis)
users.append(Alice)
educator.append(Bob)
educator.append(Chits)

x=0
while x != -1:
    x = int(input("\nEnter transaction  number, if want to exit enter -1:"))
    if x != -1:
        user_id = int(input("Enter user id: "))
        amount = int(input("Enter amount: "))
        course_name = input("Enter course name: ")
        course_id = int(input("Enter course id: "))
        challenge = secrets.token_bytes(16)
        student = input("Enter student name: ")
        educ = input("Enter educator name: ")
        student_obj = None
        edu_obj = None
        for user in users:
            if user.student_name == student:
                student_obj = user
        for edu in educator:
            if edu.educator_name == educ:
                edu_obj = edu
        transaction = {'user_id': user_id,'amount': amount,'course_name': course_name,'course_id': course_id ,'challenge': challenge, 'Student': student_obj, 'edu': edu_obj }  
        transactions.append(transaction)
    

# Create some transactions (assuming Alice does course under Bob)
# transaction1 = {'user_id': 45,'amount': 15000,'course_name': 'Blockchain','course_id': 11068 ,'challenge': secrets.token_bytes(16), 'Student': Alice, 'edu': Bob }  
# transaction2 = {'user_id': 45,'amount': 15000,'course_name': 'ML','course_id': 11065 ,'challenge': secrets.token_bytes(16), 'Student': Alice, 'edu': Bob }  
# transaction3 = {'user_id': 30,'amount': 15000,'course_name': 'Blockchain','course_id': 11068 ,'challenge': secrets.token_bytes(16), 'Student': Nis, 'edu': Bob }  
# transaction4 = {'user_id': 30,'amount': 15000,'course_name': 'ML','course_id': 11065 ,'challenge': secrets.token_bytes(16), 'Student': Nis, 'edu': Chits }  
# transaction5 = {'user_id': 45,'amount': 15000,'course_name': 'Crypto','course_id': 11069 ,'challenge': secrets.token_bytes(16), 'Student': Alice, 'edu': Chits }  

verifyTransaction = verifyTransaction()

# Verify transactions
data=[]
for transaction in transactions:
    if(verifyTransaction.verify_transaction(transaction, transaction['Student'], transaction['edu'])):
        transaction_count+=1
        data.append(transaction)
        if(transaction_count%2==0):
            miner.mineBlock(data)
            data=[]

if(len(data)!=0):
    miner.mineBlock(data)


print("////////////////////////////////////////////////////////////////////////////////")
print("\n")

def viewUser(x):
    for user in users:
        if user.sid == x:
            print("\nUSER id : ", user.sid)
            print("USER name : ", user.student_name)
            print("\n")
            for transaction in transactions:
                if transaction['user_id'] == user.sid and verifyTransaction.verify_transaction(transaction, transaction['Student'], transaction['edu']):
                    for edu in user.course_list:
                        if edu.course_id == transaction['course_id']:
                            print("Professor ID: ", edu.eid)
                            print("Professor Name: ", edu.edu_name)
                    print("Course ID: ", transaction['course_id'])
                    print("Course Name: ", transaction['course_name'])
                    print("\n")

   
def viewBlocks():
    print("\n///////////////////////////////////////////////////////////////////////////\nTraversing Blockchain")
    for block in blockchain.chain:
        print("\nBlock Index:", block.index)
        print("\nTimestamp:", block.timestamp)
        if block.index != 0:
            for transaction in block.data:
                transaction.pop('Student')
                transaction.pop('edu')
                print("\nData: ",transaction)
        print("\nPrevious Hash:", block.previous_hash)
        print("\nHash:", block.hash)


x=0
while x != -1:
    x = int(input("Enter student id to view user and their course details, -1 to exit: "))
    viewUser(x)

viewBlocks()



