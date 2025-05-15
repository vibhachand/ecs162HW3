<script lang="ts">
    import { onMount } from 'svelte';
    let output: string = '';
    onMount(() => {
      const myDate = new Date();
      const weekdays_list = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
      const months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  
      let day = weekdays_list[myDate.getDay()];
      let date = myDate.getDate();
      let month = months_list[myDate.getMonth()];
      let year = myDate.getFullYear();
  
      output = `${day}, ${month} ${date}, ${year}`;
    });
  </script>
  
  <div>{output}</div>