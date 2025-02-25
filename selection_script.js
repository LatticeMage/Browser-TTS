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
    speakButton.style.top = (lastRect.top + window.scrollY) + 10 + 'px';
    speakButton.style.zIndex = 1000;
    document.body.appendChild(speakButton);

    return speakButton
}

async function speak(text) {
    try {
        const response = await fetch('http://localhost:5000/speak', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('TTS Server Response:', data);
    } catch (error) {
        console.error('Error sending text to TTS server:', error);
    }
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
                speak(text); // Send text to TTS server

                newButton.remove();
                speakButton = null;
            });
        } else if(speakButton){
            speakButton.remove();
            speakButton = null;
        }
    } else if (speakButton){
        speakButton.remove();
        speakButton = null;
    }
}


document.addEventListener('selectionchange', handleSelectionChange);