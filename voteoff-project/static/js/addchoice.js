function addchoice() {
    var i = 1;
    name = "choice_picture".concat(i.toString());
    while (document.getElementById("choice_picture".concat(i.toString()))) {
        i++;
    }

    var div = document.getElementById('choice-list');
    var input = document.createElement('div');
    input.className = 'form-group';
    input.innerHTML = '<div class="row"><div class="col"><label for="choice_text' + i + '">Choice</label><input name="choice_text' + i
     + '" class="form-control" id="choice_text' + i + '"></div><div class="col"><label for="choice_picture' + i + '">Upload Image</label><input name="choice_picture' + i 
     + '" type="file" class="form-control-file" id="choice_picture' + i + '"></div></div>'
    div.appendChild(input);
}
