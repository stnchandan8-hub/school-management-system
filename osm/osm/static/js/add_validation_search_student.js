document.getElementById("search_student").addEventListener("submit", function(e){
let valid = true;

    // Clear previous errors
    document.getElementById("student_rollno_error3").innerHTML = "";    
     let teacher_id = document.getElementById("student_id2").value.trim();
     if(teacher_id === ""){
        document.getElementById("student_rollno_error3").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }

    })