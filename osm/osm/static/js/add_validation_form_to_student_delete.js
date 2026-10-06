console.log("delete")
document.getElementById("student_delete").addEventListener("submit", function(e){
let valid = true;

    // Clear previous errors
    document.getElementById("rollno2_error2").innerHTML = "";    
     let rollno = document.getElementById("rollno2").value.trim();
     if(rollno === ""){
        document.getElementById("rollno2_error2").innerHTML = "ID is required";
        valid = false;
         e.preventDefault();
    }

    })
