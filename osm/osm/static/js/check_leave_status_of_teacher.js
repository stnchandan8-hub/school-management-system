
document.getElementById("check_leave_status").addEventListener("submit", function(e){
    console.log('valid')
    let valid = true;

    // Clear previous errors
     document.getElementById("teacher_id_error2").innerHTML = "";
    let tid = document.getElementById("teacher_id2").value.trim();
   // Teacher ID Validation
    if(tid === ""){
        document.getElementById("teacher_id_error2").innerHTML = "Teacher id is required";
        valid = false;
         e.preventDefault();
    }
    
   
    if(!valid){
        e.preventDefault();
    }
});