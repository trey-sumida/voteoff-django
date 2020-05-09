
function disableButtons(id, len, type) {
    len++;
    if (type === "inc") {
        for (i=1; i<len; i++) {
            if (id != "inc"+i) {
                try {
                    var f = document.getElementById("inc"+i);
                    if (!f.disabled) {
                        f.setAttribute('disabled','disabled');
                    }
                } 
                catch(err) {
                    console.log("Item with id: " + i + " has already been eliminated.");
                }
            } else {
                var f = document.getElementById("dec"+i);
                f.setAttribute('disabled','disabled');
            }
        }
    } else {
        for (i=1; i<len; i++) {
            if (id != "dec"+i) {
                try {
                    var f = document.getElementById("dec"+i);
                    if (!f.disabled) {
                        f.setAttribute('disabled','disabled');
                    }
                } 
                catch(err) {
                    console.log("Item with id: " + i + " has already been eliminated.");
                }
            } else {
                var f = document.getElementById("inc"+i);
                f.setAttribute('disabled','disabled');
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
            var inc = document.getElementById("inc"+i);
            var dec = document.getElementById("dec"+i);
            if (inc.disabled || dec.disabled) {
                inc.removeAttribute("disabled")
                dec.removeAttribute("disabled")
            }
        } 
        catch(err) {
            console.log("Item with id: " + i + " has already been eliminated or is already enabled");
        }
    }
}