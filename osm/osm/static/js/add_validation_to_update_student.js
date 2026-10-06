document.getElementById("update_student").addEventListener("submit", function(e){
     let valid = true;

    // Clear previous errors
    document.getElementById("rollno_error3").innerHTML = "";
    let student_id = document.getElementById("rollno3").value.trim();
    // teacher ID Validation
    if(student_id === ""){        document.getElementById("rollno_error3").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }
    if(!valid){
        e.preventDefault();
    }
});