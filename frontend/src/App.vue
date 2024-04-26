<template>
  <div>
    <h1>Tasks</h1>
    <ul>
      <li v-for="task in tasks" :key="task.name">{{ task.name }}</li>
    </ul>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data(){
    return{
      tasks:[]
    };
  },
  mounted(){
    axios.get('http://localhost:5000/tasks')
    .then(response => {
      this.tasks = response.data;
      console.log(this.tasks);
    })
    .catch(error => {
      console.log (error);
    })
  }
  
}
</script>


