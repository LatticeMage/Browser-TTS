var speakButton;
var previousSelectionRange;

function createSpeakButton(range) {
    if (speakButton) {
        speakButton.remove();
    }

    // Get all the client rects for the selected range. It will include
    // a rect for each line
    var rects = range.getClientRects();

    // If there are rects get the last one in the list which is the rect for
    // the last line of the selection.
     var lastRect = rects.length > 0 ? rects[rects.length - 1] : range.getBoundingClientRect()

    speakButton = document.createElement("button");
    speakButton.innerHTML = "Speak";
    speakButton.style.position = 'absolute';
    speakButton.style.left =  (lastRect.right + window.scrollX) + 'px';
    speakButton.style.top = (lastRect.top + window.scrollY) + 'px';
    speakButton.style.zIndex = 1000;
    document.body.appendChild(speakButton);

    return speakButton
}

function handleSelectionChange() {
    var selection = window.getSelection();
    if (selection.rangeCount) {
        var range = selection.getRangeAt(0);
        if (range && !range.collapsed) {
             if (previousSelectionRange) {
                if ( range.startOffset === previousSelectionRange.startOffset && 
                range.startContainer === previousSelectionRange.startContainer &&
                range.endOffset === previousSelectionRange.endOffset && 
                range.endContainer === previousSelectionRange.endContainer)
                 {
                    return
                }
            }
            previousSelectionRange = range.cloneRange()
            var newButton =  createSpeakButton(range)

            newButton.addEventListener('click', function() {
                var text = selection.toString();
            
                // Send text to python
                window.speakText = text;
            
                newButton.remove();
            });
        } else if(speakButton){
            speakButton.remove();
            speakButton = null
            window.speakText = ""
        } else{
            window.speakText = ""
        }
    } else if (speakButton){
        speakButton.remove();
        speakButton = null
        window.speakText = ""
    }
}


document.addEventListener('selectionchange', handleSelectionChange);