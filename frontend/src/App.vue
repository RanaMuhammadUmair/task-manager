<template>
  <div class="app-container">
    <h1>Task Manager</h1>
    <div class="task-list">
      <div v-for="task in tasks" :key="task._id" class="task-item">
        <p>{{ task.name }}</p>
        <button class="btn-delete" @click="deleteTask(task._id)">Delete</button>
        <button class="btn-edit" @click="editTask(task._id)">Edit</button>
      </div>
    </div>
    <div class="add-task">
      <input v-model="newTask" placeholder="Add new task" class="task-input">
      <button @click="addTask" class="btn-add">Add Task</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tasks: [],
      newTask: ''
    };
  },
  methods: {
    fetchTasks() {
  axios.get('http://localhost:5000/tasks')
    .then(response => {
      console.log('Tasks fetched:', response.data); // Check the fetched data
      
      this.tasks = response.data; // Assign the data to the tasks array
      this.$forceUpdate();
  
    })
    .catch(error => {
      console.error('Error fetching tasks:', error); // Log any errors
    });
}
,
addTask() {
  axios.post('http://localhost:5000/tasks', { name: this.newTask })
    .then(response => {
      this.tasks.push({ _id: response.data._id, name: this.newTask });  // Append the new task
      this.newTask = '';  // Reset the input field
      this.fetchTasks();
    })
    .catch(error => {
      console.error('Error adding task:', error);
    });
}
,
    deleteTask(taskId) {
  if (!taskId) {
    console.error('Task ID is undefined');
    return;
  }
  axios.delete(`http://localhost:5000/tasks/${taskId}`)
    .then(() => {
      this.fetchTasks();  // Refresh the list after deleting
    })
    .catch(error => {
      console.error('Error deleting task:', error);
    });
}
,
editTask(taskId) {
  let newName = prompt("Enter new task name:", "");
  if (newName !== null && newName !== "") {
    console.log(`Attempting to edit task with ID: ${taskId}`); // Debugging log
    axios.put(`http://localhost:5000/tasks/${taskId}`, {name: newName})
      .then(() => {
        this.fetchTasks();  // Refresh the list after editing
      })
      .catch(error => {
        console.error('Error updating task:', error);
      });
  }
}
,
created() {
  this.fetchTasks();
},
mounted(){
  this.fetchTasks();
  
}

}}

</script>


<style scoped>
.app-container {
  width: 80%;
  margin: auto;
  max-width: 600px;
}

.task-list {
  margin: 20px 0;
}

.task-item {
  background: #f3f3f3;
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.btn-delete, .btn-edit {
  margin-left: 10px;
}

.add-task {
  display: flex;
  margin-top: 20px;
}

.task-input {
  flex-grow: 1;
  margin-right: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-add {
  padding: 10px 20px;
  background: #5cb85c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-add:hover {
  background: #4cae4c;
}

</style>


