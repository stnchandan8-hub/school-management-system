console.log("delete")
document.getElementById("delete_teachers").addEventListener("submit", function(e){
let valid = true;

    // Clear previous errors
    document.getElementById("teacher_id_errors").innerHTML = "";    
     let teacher_id = document.getElementById("teacher_ids").value.trim();
     if(teacher_id === ""){
        document.getElementById("teacher_id_errors").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }

    })
