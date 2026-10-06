console.log("validation")
document.getElementById("sf_delete").addEventListener("submit", function(e){
     let valid = true;

    // Clear previous errors
    document.getElementById("semail_id_error").innerHTML = "";
    let teacher_id = document.getElementById("semail_id").value.trim();
    // teacher ID Validation
    if(teacher_id === ""){        document.getElementById("semail_id_error").innerHTML = "Email is required";
        valid = false;
         e.preventDefault();
    }
    if(!valid){
        e.preventDefault();
    }
});