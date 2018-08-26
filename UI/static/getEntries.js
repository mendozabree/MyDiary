let token = document.cookie;
function getEntries() {
    fetch('http://127.0.0.1:5000/api/v1/entries', {
        method: 'GET',
        headers: {Authorization : `Bearer ${document.cookie}`}
    })
        .then((response) => response.json())
        .then(function (data) {
			if (data['status'] === 'Success') {
			    let heading = document.createElement("h2")
			    if (data['message'] === 'You have no entries yet!'){
			        heading.innerText = 'You have no entries, start today by clicking New Entry above.'
                    document.getElementById('myEntries').appendChild(heading)
                }else {
			        heading.innerText = 'Here are your entries!'
                    document.getElementById('myEntries').appendChild(heading)
                    // console.log(data)
                    addElement(data)
                    sortEntries()
                }
			}else{
			    location.href='unauthorized.html'
				//alert(data['msg'])
			}
        })
}
function addElement (entries) {
    let myArray = entries['message'];
    let entriesLength = myArray.length;

    for (let i=0; i<entriesLength; i++){
        let row1 = createDiv('row titleBlock');
        let row2 = createDiv('row');
        let row3 = createDiv('row');
        let col0 = createDiv('col-12 entry');
        let col1 = createDiv('col-6 col-m-6');
        let col2 = createDiv('col-1 col-m-1');
        let col3 = createDiv('col-3 col-m-3');
        let col4 = createDiv('col-12');
        let col5 = createDiv('col-8 col-m-8');
        let col6 = createDiv('col-2 col-m-2');
        let col7 = createDiv('col-2');
        let col8 = createDiv('col-2 col-m-2')

  	    let newTitleLabel = document.createElement("label")
  	    let newContentLabel = document.createElement("div")
        let newDateLabel = document.createElement("label")
        let newTimeLabel = document.createElement("label")
  	    let viewbtn = document.createElement("button")

        let timestamp = parseInt(entries['message'][i][5])* 1000
        let currentTimestamp = new Date().getTime()
        if ((currentTimestamp-timestamp) < 86400000){
            let editbtn = document.createElement("button")
            editbtn.innerHTML = 'Edit Entry'
            editbtn.id = 'edit'+entries['message'][i][0]
            editbtn.setAttribute('class', 'edit-btn')
            col8.appendChild(editbtn)
        }
        let dateTime = new Date(entries['message'][i][3])
        let dateOnly = dateTime.toDateString()

  	    let newContent = document.createTextNode(entries['message'][i][2])
        let newDateContent = document.createTextNode(dateOnly)
        let newTimeContent = document.createTextNode(entries['message'][i][4])
        let newTitle = document.createTextNode(entries['message'][i][1])
  	    viewbtn.innerHTML = 'Read Entry'
  	    viewbtn.id = 'view'+entries['message'][i][0]
        col0.id = 'div-'+entries['message'][i][0]

        viewbtn.setAttribute("class","primary-btn")
        newTitleLabel.setAttribute("class", "date-label")
        newDateLabel.setAttribute("class", "date-label")
        newTimeLabel.setAttribute("class", "date-label")
  	    newContentLabel.id = 'myEntry'+entries['message'][i][0]
        newContentLabel.setAttribute('class', 'sampleText')

  	    newTitleLabel.appendChild(newTitle)
  	    newContentLabel.appendChild(newContent)
        newDateLabel.appendChild(newDateContent)
        newTimeLabel.appendChild(newTimeContent)
        col1.appendChild(newTitleLabel)
        col7.appendChild(newTimeLabel)
        col3.appendChild(newDateLabel)
        row1.appendChild(col1)
        row1.appendChild(col2)
        row1.appendChild(col3)
        row1.appendChild(col7)
        col4.appendChild(newContentLabel)
        row2.appendChild(col4)
        col6.appendChild(viewbtn)
        row3.appendChild(col5)
        row3.appendChild(col6)
        row3.appendChild(col8)
        col0.appendChild(row1)
        col0.appendChild(row2)
        col0.appendChild(row3)

        let htmlDiv=document.getElementById('myEntries')
  	    htmlDiv.insertBefore(col0,document.getElementsByTagName('h2').nextSibling)
  }
  // function createRow(){
  //     let row = document.createElement('div')
  //     row.setAttribute('class', 'row')
  //     return row
  // }
  function createDiv(styleClass){
      let col = document.createElement('div')
      col.setAttribute('class', styleClass)
      return col
  }
  document.getElementById("myEntries").addEventListener("click", myFunction, false);
  function myFunction(e){
	  if (e.target !== e.currentTarget){
		//console.log(e.target.id.length)
		  let entryId = e.target.id;
		  let firstLetter = entryId.charAt(0);
		  console.log(firstLetter)
		  if (firstLetter === 'v'){
			  let myId = getInt(e.target.id,4);
			  localStorage.setItem("viewEntryId", myId)
              // viewSpecific()
			  location.href='my_entry.html'
		  }
		  if (firstLetter === 'e'){
		      let editId = getInt(e.target.id,4);
			  localStorage.setItem("editEntryId", editId);
			  localStorage.setItem("editClicked", "true")
              // viewSpecific()
			  location.href='new_entry.html'
          }
		// let clickedItem = e.target.id;
		// alert("Hello "+clickedItem);
	}
	  // e.stopPropagation();
  }
}
function getInt(myString,lenString){
    let myInt = myString.slice(lenString)
    return parseInt(myInt)
}
function sortEntries() {
    let idList = document.getElementById('myEntries').children;
    idList = Array.prototype.slice.call(idList, 1);

    idList.sort(function(a,b) {
      let aord = +a.id.split('-')[1];
      let bord = +b.id.split('-')[1];
      return (aord<bord)? 1:-1;
    });
    let parent = document.getElementById("myEntries");
    let myDiv1 = document.getElementsByTagName('h2');
    myDiv1.innerHTML = 'Here are all your entries!'
    for (let i=0, l = idList.length; i <l; i++){
      parent.appendChild(idList[i]);
    }
}