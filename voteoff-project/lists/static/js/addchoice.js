function addchoice() {
    var newChoiceInput = document.createElement("LI");
    selectNode = `
    <div class="form-group">
    <label for="choice_text">Choice</label>
    <input name="choice_text" class="form-control" id="choice_text">
    </div>
    `;
    newChoiceInput.innerHTML = selectNode;
    
    var choice_list = document.getElementById("choice-list");
    choice_list.insertBefore(newChoiceInput, document.getElementById("add-choice-li"));
}