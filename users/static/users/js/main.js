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
        document.getElementById('form').append(submit_button);

        // remove add items button when the delete items button is clicked
        let add_text_button = document.getElementById("add-text-button");
        add_text_button.parentNode.removeChild(add_text_button);

        // also remove the delete items button, because we will add a submit button to our form
        if (document.getElementById("delete-items-button") != null) {
            let delete_items_button = document.getElementById("delete-items-button");
            delete_items_button.parentNode.removeChild(delete_items_button);
        }

        // create cancel button
        let cancel_button = document.createElement("button");
        cancel_button.id = "cancel";
        cancel_button.name = "cancel";
        cancel_button.className = "btn btn-dark";
        cancel_button.innerHTML = "cancel";
        cancel_button.value = "true";
        document.getElementById("form").append(cancel_button);
    }

    // adds item to grocery list
    function addText() {
        // create text field
        const text_field = document.createElement("input");
        text_field.setAttribute("type", "text");
        text_field.setAttribute("name", "added-text");
        text_field.className = "form-control";

        // add text field and submit button to html
        document.getElementById('form').append(text_field);

        addSubmitAndCancel();
    }

    // adds delete boxes for items in grocery list the first time button is pressed, then deletes them the second time it's pressed
    function deleteItems() {
        // when we press delete items, check boxes are added
        let list = document.getElementById('list').getElementsByTagName('li');

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

    // button for adding item text to grocery list
    if (document.getElementById('add-text-button') != null) {
        document.getElementById('add-text-button').onclick = addText;
    }

    // button for adding delete boxes of items in grocery list
    if (document.getElementById('delete-items-button') != null) {
        document.getElementById('delete-items-button').onclick = deleteItems;
    }

    // button for accepting friend request
    if (document.getElementById('friend-requests-list') != null) {
        let request_list = document.getElementById('friend-requests-list').getElementsByTagName('li');
        let button_list = document.getElementById('friend-requests-list').getElementsByTagName('button');
        for (let i=0; i<button_list.length; i++) {
            button_list[i].onclick = function () {
                if (i % 2 == 0) {
                    index = Math.floor(i/2);
                    let accept_user = request_list[index].getElementsByTagName('span')[0].innerHTML;
                    console.log('accept', accept_user);

                    // we have to create csrf_token because we are sending post data
                    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
                    console.log(csrf_token);

                    // create xml object that we can use to send data to our django views, and then models
                    var request = new XMLHttpRequest();
                    request.open("POST", 'add_friend_request', true);
                    request.setRequestHeader("X-CSRFToken", csrf_token);

                    // create data to return back to our 
                    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
                    data = 'accept_user=';
                    data += accept_user;
                    request.send(data);
                    console.log(request);
                    window.location.href = '/friends/';
                }
                else {
                    index = Math.floor(i/2);
                    let decline_user = request_list[index].getElementsByTagName('span')[0].innerHTML
                    console.log('decline', decline_user);

                    // we have to create csrf_token because we are sending post data
                    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
                    console.log(csrf_token);

                    // create xml object that we can use to send data to our django views, and then models
                    var request = new XMLHttpRequest();
                    request.open("POST", 'remove_friend_request', true);
                    request.setRequestHeader("X-CSRFToken", csrf_token);

                    // create data to return back to our 
                    request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
                    data = 'remove_user=';
                    data += decline_user;
                    request.send(data);
                    console.log(request);
                    window.location.href = '/friends/';
                }
            }
        }
    }
}