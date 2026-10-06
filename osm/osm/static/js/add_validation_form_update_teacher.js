console.log("validation")
document.getElementById("update_teacher").addEventListener("submit", function(e){
     let valid = true;

    // Clear previous errors
    document.getElementById("teacher_id_error1").innerHTML = "";
    let teacher_id = document.getElementById("teacher_id1").value.trim();
    // teacher ID Validation
    if(teacher_id === ""){        document.getElementById("teacher_id_error1").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }
    if(!valid){
        e.preventDefault();
    }
});