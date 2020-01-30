document.addEventListener('DOMContentLoaded', onDOMContentLoaded);

function onDOMContentLoaded() {

    // adds item to grocery list
    function addText() {
        if (add_item) {
            // create text field
            const text_field = document.createElement("input");
            text_field.setAttribute("type", "text");
            text_field.setAttribute("name", "added-text");

            // create submit button for text field
            const submit_text = document.createElement("button");
            submit_text.setAttribute("id", "submit-text");
            submit_text.innerHTML = 'submit';

            // add text field and submit button to html
            document.getElementById('new-item-form').append(text_field, submit_text);
            console.log('in the addText function');
        }
        add_item = false;
    }

    // adds delete boxes for items in grocery list the first time button is pressed, then deletes them the second time it's pressed
    function deleteItems() {

        // the first time we press delete items check boxes are added
        if (delete_boxes()) {
            let list = document.getElementById('grocery-list').getElementsByTagName('li');

            for (var i = 0, len = list.length; i < len; i++) {
                // create check box for every item in our list
                delete_box = document.createElement("input");
                delete_box.setAttribute("type", "checkbox");
                // we name our checkbox with its corresponding item name
                delete_box.setAttribute("name", list[i].innerHTML);

                list[i].append(delete_box);
            }
        }
        // the second time the delete items button is pressed the items checked are deleted
        else {
            // if (confirm('Are you sure you want to delete checked items?')) {
            if (true) {
                // create list of boxes for each of our list items
                let boxes = document.getElementById('grocery-list').getElementsByTagName('input');

                // we need to append our list to our form tag to grab the post data in our views.py
                let form = document.getElementById('new-item-form');
                for (let i = 0; i < boxes.length; i++) {
                    clone = boxes[i].cloneNode(true);
                    // clone.setAttribute('type', 'hidden');
                    // clone.type = 'hidden';
                    form.append(clone);
                }
                console.log(form);
                
                // create submit button for text field
                const delete_items_button = document.createElement("button");
                delete_items_button.setAttribute("id", "submit-deleted-items");
                delete_items_button.setAttribute("type", "submit");
                delete_items_button.innerHTML = 'submit';
                document.getElementById('new-item-form').append(delete_items_button);
            }

        }
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
    if (document.getElementById('add-text') != null) {
        document.getElementById('add-text').onclick = addText;
    }

    // button for adding delete boxes of items in grocery list
    if (document.getElementById('delete-items') != null) {
        document.getElementById('delete-items').onclick = deleteItems;
    }

    // initialize delete_boxes to false
    let delete_boxes = reverseBool();

    // initialize add item button to false, this is used so that users can only press 'Add item' once
    let add_item = true;
}
