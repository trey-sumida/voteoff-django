
function disableButtons(id, len) {
    var e = document.getElementById(id);
    if (e.checked) {
        console.log("checked");
        len++;
        for (i=1; i<len; i++) {
            if (id != i) {
                try {
                    var f = document.getElementById(i);
                    if (!f.disabled) {
                        f.setAttribute('disabled','disabled');
                    }
                } 
                catch(err) {
                    console.log("Item with id: " + i + " has already been eliminated.");
                }
            }
        }
    }
}

function reset_function(len) {
    var e = document.getElementById("list");
    e.reset();
    len++;
    for (i=1; i<len; i++) {
        try {
            var f = document.getElementById(i);
            if (f.disabled) {
                f.removeAttribute("disabled")
            }
        } 
        catch(err) {
            console.log("Item with id: " + i + " has already been eliminated or is already enabled");
        }
    }
}