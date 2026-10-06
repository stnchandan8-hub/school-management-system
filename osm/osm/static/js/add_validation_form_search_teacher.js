document.getElementById("search_teacher").addEventListener("submit", function(e){
let valid = true;

    // Clear previous errors
    document.getElementById("teacher_id_error2").innerHTML = "";    
     let teacher_id = document.getElementById("teacher_id2").value.trim();
     if(teacher_id === ""){
        document.getElementById("teacher_id_error2").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }

    })