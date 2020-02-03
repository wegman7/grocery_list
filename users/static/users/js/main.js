document.addEventListener('DOMContentLoaded', onDOMContentLoaded);

function onDOMContentLoaded() {

    // addes submit and cancel, and removes add item and delete item buttons
    function addSubmitAndCancel() {
        // create submit button
        const submit_button = document.createElement("button");
        submit_button.setAttribute("id", "submit");
        submit_button.className = "btn";
        // add danger styling to submit button only when deleting items
        if (document.getElementsByName("added-text").length == 0) { submit_button.className = submit_button.className.concat(" btn-danger"); }
        else { submit_button.className = submit_button.className.concat(" btn-dark"); }
        submit_button.innerHTML = 'submit';
        document.getElementById('new-item-form').append(submit_button);

        // remove add items button when the delete items button is clicked
        let add_text_button = document.getElementById("add-text-button");
        add_text_button.parentNode.removeChild(add_text_button);

        // also remove the delete items button, because we will add a submit button to our form
        let delete_items_button = document.getElementById("delete-items-button");
        delete_items_button.parentNode.removeChild(delete_items_button);

        // create cancel button
        let cancel_button = document.createElement("button");
        cancel_button.id = "cancel";
        cancel_button.name = "cancel";
        cancel_button.className = "btn btn-dark";
        cancel_button.innerHTML = "cancel";
        cancel_button.value = "true";
        document.getElementById("new-item-form").append(cancel_button);
    }

    // adds item to grocery list
    function addText() {
        // create text field
        const text_field = document.createElement("input");
        text_field.setAttribute("type", "text");
        text_field.setAttribute("name", "added-text");
        text_field.className = "form-control";

        // add text field and submit button to html
        document.getElementById('new-item-form').append(text_field);

        addSubmitAndCancel();
    }

    // adds delete boxes for items in grocery list the first time button is pressed, then deletes them the second time it's pressed
    function deleteItems() {
        // when we press delete items, check boxes are added
        let list = document.getElementById('grocery-list').getElementsByTagName('li');

        for (var i = 0, len = list.length; i < len; i++) {
            // create check box for every item in our list
            let delete_box = document.createElement("input");
            delete_box.setAttribute("type", "checkbox");
            // we name our checkbox with its corresponding item name
            delete_box.setAttribute("name", list[i].innerHTML);

            list[i].prepend(' ');
            list[i].prepend(delete_box);
        }
        addSubmitAndCancel();
    }

    // closure that reverses bool value
    function reverseBool() {
        bool = false;
        return function() {
            return bool = !bool;
        }
    }

    // button for submitting login form
    if (document.getElementById('submit-login') != null) {
        document.getElementById('submit-login').onclick = sub;
    }

    // button for adding item text to grocery list
    if (document.getElementById('add-text-button') != null) {
        document.getElementById('add-text-button').onclick = addText;
    }

    // button for adding delete boxes of items in grocery list
    if (document.getElementById('delete-items-button') != null) {
        document.getElementById('delete-items-button').onclick = deleteItems;
    }
}