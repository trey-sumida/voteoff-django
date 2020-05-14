function addchoice() {
    var newChoiceInput = document.createElement("LI");
    selectNode = `
    <div class="form-group">
    <div class="row">
    <div class="col">
      <label for="choice_text">Choice</label>
      <input name="choice_text" class="form-control" id="choice_text">
    </div>
    <div class="col">
      <label for="choice_picture">Upload image</label>
      <input type="file" class="form-control-file" id="choice_picture" name="choice_picture">
    </div>
</div>
    </div>
    `;
    newChoiceInput.innerHTML = selectNode;
    
    var choice_list = document.getElementById("choice-list");
    choice_list.insertBefore(newChoiceInput, document.getElementById("add-choice-li"));
}