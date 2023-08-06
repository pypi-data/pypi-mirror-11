/**
 * Created by phg49389 on 6/18/15.
 */
String.prototype.contains = function (it) {
    return this.indexOf(it) != -1;
};

//This method is called when another instance of a multiple div is being added.
//This block of code takes in HTML code, finds all ids in that code, and adds "_#" right after the ids to make it unique when the new code gets inserted
function incrementIDs(code_to_update, num_times_instantiated) {
    var arr_of_words = code_to_update.split(" ");
    var to_return = " ";
    var i;
    //Edit the ids of all the elements
    for (i = 0; i < arr_of_words.length; i++) {
        //Replace all quotes with tics to keep JS happy
        arr_of_words[i] = arr_of_words[i].replace(/"/g, '`');
        if (arr_of_words[i].indexOf("id") == 0) {
            arr_of_words[i] = arr_of_words[i].substring(0, arr_of_words[i].length - 1) + "_" + num_times_instantiated + arr_of_words[i].substring(arr_of_words[i].length - 1, arr_of_words[i].length);
        }
        else if (arr_of_words[i].indexOf("onclick") == 0) {
            arr_of_words[i] = arr_of_words[i].substring(0, arr_of_words[i].length - 4) + "_" + num_times_instantiated + arr_of_words[i].substring(arr_of_words[i].length - 4, arr_of_words[i].length);
        }
        arr_of_words[i] = arr_of_words[i].replace(/`/g, '\"');
        //Put the quotes back
        to_return += arr_of_words[i] + " ";
    }
    //If there's a script, update its variables appropriately
    //If there's a button, update its onclick method appropriately
    arr_of_words = to_return.split("<");
    to_return = " ";
    var match = "";
    var pattern = /ext\d(_\d)*/g;
    var arr_of_scripts = [];
    for (i = 0; i < arr_of_words.length; i++) {
        //Replace all quotes with tics to keep JS happy
        arr_of_words[i] = arr_of_words[i].replace(/"/g, '`');
        if (arr_of_words[i].indexOf("script") == 0) {
            //The only way to create new scripts in JS, add them to existing HTML, and have it work is to append it to the HMTL at the very end,
            //so this little section takes the existing scripts, increments the ids appropriately, and then stores it in an array to be returned
            match = arr_of_words[i].match(pattern)[0];
            var script = document.createElement("script");
            script.type = "text/javascript";                                               //"<script" has 7 chars
            script.text = arr_of_words[i].replace(pattern, match + "_" + num_times_instantiated).substring(7).replace(/`/g, '\"');
            arr_of_scripts.push(script);
        }
        //Put the quotes back
        arr_of_words[i] = arr_of_words[i].replace(/`/g, '\"');
        if (arr_of_words[i].contains(">")) {//If it's a tag
            to_return += "<" + arr_of_words[i];
        }
        else {//It's just an attribute or internal content
            to_return += arr_of_words[i];
        }
    }
    to_return = [to_return + "<br/>"];
    for (i = 0; i < arr_of_scripts.length; i++) {
        to_return.push(arr_of_scripts[i]);
    }
    //Now to_return is [code to return + <br/>, script1, script2, ...]
    return to_return;
}

//This array keeps track of the current set of folders and files being looked at. It gets updated by fetchArrayFromCascade,
//and then used by constructInternalDisplay
var arrayOfContents = [];

//Ajax! Because HTML/JS can't access Cascade directly, instead it hands the call off to Python, which then returns
//a JSON array that JS can handle. By default, it wants the top-level folder, "/", but if a path is passed through to it ("/_blink-content")
//then it can handle that as well. typeOfFile filters the results being displayed, but that filtering is actually done in constructInternalDisplay.
//However, because constructInternalDisplay and this method call each other, the typeOfFile must continue to be passed between the two. It is
//originally set in forms.py in build_page, in the "asset" elif statement. idOfButtonThatCalledMe is passed on to constructInternalDisplay
//so that once an asset is chosen, that button can have its value set to the filepath so that the user can see their choice, as well as storing
//it cleverly for submit.
function fetchArrayFromCascade(path, typeOfFile, username, idOfButtonThatCalledMe) {
    var alias = document.getElementById("divToAddTableTo");
    var loadingGif = document.createElement("img");
    loadingGif.setAttribute("src","http://i.imgur.com/zOAq6uk.gif");
    var currentMenu = alias.lastElementChild;
    alias.replaceChild(loadingGif, alias.lastElementChild);
    var urlToSend = "fetch";
    if (path != "") {
        urlToSend += path;
    }
    urlToSend += "?username="+username;
    $.ajax({
        type: "POST",
        url: urlToSend
    }).done(function (response) {
        arrayOfContents = JSON.parse(response);
        if (arrayOfContents.length == 0) {
            alert("Empty folder");
            alias.replaceChild(currentMenu, alias.lastElementChild);
        }
        else {
            constructInternalDisplay(typeOfFile, username, idOfButtonThatCalledMe);
        }
        //Stop the loading gif now?
    });
}

//This method's parameters are explained above fetchArrayFromCascade(), so this will just explain the method itself.
//When an asset has to be chosen, a modal is displayed above the page. This method constructs the table that gets
//displayed in that modal. The header of this table has the button to go up a folder and the filepath of the directory
//that is being displayed right now, and the body of the table is set up as such: if the type is a folder, then the row
//displayed is a + button that changes the modal to view that folder and the name of the folder. If it's not a folder,
//then it checks the file's type. If the type matches the type desired, it displays it as a button that will change
//the asset's button's value to the filepath chosen.
function constructInternalDisplay(typeOfFileToChoose, username, idOfButtonThatCalledFetch) {
    var filepath = arrayOfContents[0].split('~')[1];
    var parent_path = filepath.substring(0, filepath.lastIndexOf("/"));
    var toReturn = document.createElement("table");
    toReturn.rules = "groups";
    toReturn.frame = "box";
    //Make the header
    var head = document.createElement("thead");
    var leftElemToAdd = document.createElement("th");
    var goBack = document.createElement("button");
    goBack.innerHTML = "Go up a folder";
    goBack.setAttribute("onclick", "fetchArrayFromCascade(\'" + parent_path + "\',\'" + typeOfFileToChoose
        + "\',\'" + username + "\', \'" + idOfButtonThatCalledFetch + "\');");
    leftElemToAdd.appendChild(goBack);
    var rightElemToAdd = document.createElement("th");
    rightElemToAdd.innerHTML = filepath;
    if (filepath == "/") {
        filepath = "";
        goBack.setAttribute("disabled", "true");
    }
    var rowToAdd = document.createElement("tr");
    rowToAdd.appendChild(leftElemToAdd);
    rowToAdd.appendChild(rightElemToAdd);
    head.appendChild(rowToAdd);
    toReturn.appendChild(head);
    //Make the body
    var body = document.createElement("tbody");
    var insert = false;
    for (var i = 1; i < arrayOfContents.length; i++) {
        rowToAdd = document.createElement("tr");
        leftElemToAdd = document.createElement("td");
        rightElemToAdd = document.createElement("td");
        var thisType = arrayOfContents[i].split("~")[0];
        var thisName = arrayOfContents[i].split("~")[1];
        if (thisType == 'folder') {
            //It's a subfolder
            var subfolder = document.createElement("button");
            subfolder.innerHTML = "+";
            subfolder.style = "float:right";
            subfolder.setAttribute("onclick", "fetchArrayFromCascade(\'" + filepath + "/" + thisName + "\',\'" + typeOfFileToChoose + "\',\'"
                + username + "\', \'" + idOfButtonThatCalledFetch + "\');");
            leftElemToAdd.appendChild(subfolder);
            rightElemToAdd.innerHTML = thisName;
            insert = true;
        }
        else if (thisType.contains(typeOfFileToChoose)) {
            //It's a file to choose
            leftElemToAdd.innerHTML = "";
            var submit = document.createElement("button");
            submit.innerHTML = thisName;
            submit.setAttribute("onclick", "submitAssetChoice(\"" + filepath + "/" + thisName + "\",\"" + idOfButtonThatCalledFetch + "\");");
            submit.setAttribute("data-dismiss", "modal");
            rightElemToAdd.appendChild(submit);
            insert = true;
        }
        if (insert) {
            rowToAdd.appendChild(leftElemToAdd);
            rowToAdd.appendChild(rightElemToAdd);
            body.appendChild(rowToAdd);
            insert = false;
        }
    }
    toReturn.appendChild(body);
    var alias = document.getElementById("divToAddTableTo");
    alias.replaceChild(toReturn, alias.lastElementChild);
    $("#myModal").modal();
}

//This method is pretty self-explanatory. It gets called by the file-type buttons in the modal, and its job is to change
//the value of the button that called the modal to the filepath chosen by the user.
function submitAssetChoice(fullFilePath, idToChange) {
    document.getElementById(idToChange).setAttribute("value", fullFilePath);
}

function submitForm(){
    var formHead = document.getElementById("datadefform");
    var array_of_results = [];
    var id, val;
    for(var i = 0; i < formHead.elements.length; i++){
        id = formHead.elements[i].id;
        val = formHead.elements[i].value;
        if(id.contains("addTo") || id.contains("removeFrom") || id == "") {}
        else{
            array_of_results.push(id + "=" + val);
        }
    }
    $.ajax({
        type: "POST",
        url: "submit",
        data: { data_pairs: JSON.stringify(array_of_results) }
    }).done(function (response) {
        var address = window.location.href;
        var base = address.slice(0,address.indexOf("?")-1);
        base += "/" + response;
        window.location.href = base;
    });
}

