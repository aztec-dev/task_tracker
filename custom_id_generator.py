class CustomIdGenerator:
    def __init__(self, counter=0):
        self.counter = counter
    
    def __str__(self):
        return f"{self.counter}"
    
    def generate_task_id(self):
        # Increment counter and return a unique ID
        self.counter += 1
        return self.counter

# Tests
# generator = CustomIdGenerator()
# print(generator.generate_task_id())
# print(generator.generate_task_id())