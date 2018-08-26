// let entries = {'message':[[1,'entry1','myFirst', '12 Aug 1995'],[2,'entry2','mySecond','1 Aug 1995'],[3,'entry3','myThird', '12 Sept 1995']]}

function addElement (entries) {
  let myArray = entries['message'];
  let entriesLength = myArray.length;

  for (let i=0; i<entriesLength; i++){
      let row1 = createRow();
      let row2 = createRow();
      let row3 = createRow();
      let col0 = createCol('col-12 entry');
      let col1 = createCol('col-8 col-m-8');
      let col2 = createCol('col-1 col-m-1');
      let col3 = createCol('col-3 col-m-3');
      let col4 = createCol('col-12');
      let col5 = createCol('col-9 col-m-8');
      let col6 = createCol('col-3 col-m-4');

  	  let newTitleLabel = document.createElement("label")
  	  let newContentLabel = document.createElement("label")
      let newDateLabel = document.createElement("label")
  	  let editbtn = document.createElement("button")
  	  let viewbtn = document.createElement("button")

  	  let newContent = document.createTextNode(entries['message'][i][1])
      let newDateContent = document.createTextNode(entries['message'][i][3])
      let newTitle = document.createTextNode(entries['message'][i][2])
  	  viewbtn.innerHTML = 'View'
  	  editbtn.innerHTML = 'Edit'
  	  viewbtn.id = 'view'+entries['message'][i][0]
  	  editbtn.id = 'edit'+entries['message'][i][0]

      viewbtn.setAttribute("class","primary-btn")
      newTitleLabel.setAttribute("class", "date-label")
      newDateLabel.setAttribute("class", "date-label")
  	  newContentLabel.id = 'myEntry'+entries['message'][i][0]

  	  newTitleLabel.appendChild(newTitle)
  	  newContentLabel.appendChild(newContent)
      newDateLabel.appendChild(newDateContent)
      col1.appendChild(newTitleLabel)
      col3.appendChild(newDateLabel)
      row1.appendChild(col1)
      row1.appendChild(col2)
      row1.appendChild(col3)
      col4.appendChild(newContentLabel)
      row2.appendChild(col4)
      col6.appendChild(viewbtn)
      col6.appendChild(editbtn)
      row3.appendChild(col5)
      row3.appendChild(col6)
      col0.appendChild(row1)
      col0.appendChild(row2)
      col0.appendChild(row3)

      let htmlDiv=document.getElementById('myEntries')
  	  htmlDiv.appendChild(col0)
  }
  function createRow(){
      let row = document.createElement('div')
      row.setAttribute('class', 'row')
      return row
  }
  function createCol(styleClass){
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
		  if (firstLetter === 'v' || firstLetter === 'e'){
			  let myId = getInt(e.target.id,4);
			  localStorage.setItem("entryId", myId)
		  }
		  else{
		      alert("Hey")
		  }
		// let clickedItem = e.target.id;
		// alert("Hello "+clickedItem);
	}
	  e.stopPropagation();}
}
function getInt(myString,lenString){
	let myInt = myString.slice(lenString)
    return parseInt(myInt)
}