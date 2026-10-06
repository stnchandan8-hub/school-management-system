
document.getElementById("check_status").addEventListener("submit", function(e){
    console.log('valid')
    let valid = true;

    // Clear previous errors
     document.getElementById("teacher_id_error1").innerHTML = "";
    let tid = document.getElementById("teacher_id1").value.trim();
   // Teacher ID Validation
    if(tid === ""){
        document.getElementById("teacher_id_error1").innerHTML = "Teacher id is required";
        valid = false;
         e.preventDefault();
    }
    
   
    if(!valid){
        e.preventDefault();
    }
});