import hashlib

# Hàm băm (hash function) dùng SHA-1 rồi modulo 2^m để ánh xạ key và node ID vào vòng Chord
def hash_key(key, m=4):
    return int(hashlib.sha1(str(key).encode()).hexdigest(), 16) % (2 ** m)

# Lớp Node mô phỏng một nút trong hệ thống Chord
class Node:
    def __init__(self, node_id, m=4):
        self.id = node_id        
        self.m = m               
        self.successor = self    
        self.predecessor = None  

    # Hàm tìm successor của một key (ai chịu trách nhiệm lưu key này?)
    def find_successor(self, key_id):
        # Trường hợp key nằm giữa node hiện tại và successor
        if self.id < key_id <= self.successor.id or \
           (self.id > self.successor.id and (key_id > self.id or key_id <= self.successor.id)):
            return self.successor
        else:
            # Nếu không thì chuyển tiếp việc tìm kiếm sang successor
            return self.successor.find_successor(key_id)

    # Hàm join: thêm node mới vào vòng (dựa trên một node đã tồn tại)
    def join(self, existing_node):
        if existing_node:
            self.successor = existing_node.find_successor(self.id)
        else:
            self.successor = self  

# Hàm setup_chord: thiết lập vòng Chord với danh sách node ban đầu
def setup_chord(nodes):
    # Sắp xếp node theo ID
    nodes.sort(key=lambda n: n.id)
    # Gán successor cho từng node
    for i in range(len(nodes)):
        nodes[i].successor = nodes[(i+1) % len(nodes)]
    return nodes

# Phần main demo
if __name__ == "__main__":
    m = 4  
    node_ids = [0, 1, 4, 5]  
    nodes = [Node(n, m) for n in node_ids]
    nodes = setup_chord(nodes)

    print("Chord ring:")
    for n in nodes:
        print(f"Node {n.id} -> Successor {n.successor.id}")

    print("\nLookup results:")
    # Thử lookup một số key
    test_keys = [2, 7, 14]
    for k in test_keys:
        start_node = nodes[0]  # bắt đầu tìm từ Node 0
        succ = start_node.find_successor(k)
        print(f"Key {k} is stored at Node {succ.id}")
