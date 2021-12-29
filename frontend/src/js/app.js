import FetchService from './service/FetchService';

/*-- Objects --*/
const fetchService = new FetchService();
/*-- /Objects --*/

/*-- On Load -- */
if (window.location.href.includes('/success')) {
  const queryString = window.location.search;
  const encodedResponse = queryString.split("?res=")[1];
  const decodedResponse = decodeURIComponent(encodedResponse);
  const responseJSON = JSON.parse(decodedResponse);

  const sourceName = responseJSON.source.name;
  const sourceUsername = responseJSON.source.username;
  const targetName = responseJSON.target.name;
  const targetUsername = responseJSON.target.username;
  const followersFollowed = Array.from(responseJSON.followers_followed);
  const count = followersFollowed.length;

  // 1. Set title text on success page
  var titleTxt;
  var descriptionTxt;
  if (count > 0) {
    // titleTxt = `You're legitimate!`;
    titleTxt = `@${targetUsername} follows ${count} of @${sourceUsername}'s followers:`
  } else{
    // titleTxt = `You're not there yet, but keep working on it!`;
    titleTxt = `@${targetUsername} does not follow any of @${sourceUsername}'s followers:`
  }
  // if (count > 1) {
  //   titleTxt = `Found ${count} followers!`;
  // } else if (count === 1) {
  //   titleTxt = `Found 1 follower!`;
  // } else {
  //   titleTxt = `No followers found`;
  // }
  // if (count > 1) {
  //   titleTxt = `${targetName} follows ${count} accounts that follow ${sourceName}`;
  // } else if (count === 1) {
  //   titleTxt = `${targetName} follows 1 account that follows ${sourceName}`;
  // } else {
  //   titleTxt = `${targetName} does not follow anyone that follows ${sourceName}`;
  // }
  document.getElementById('lblTitle').innerHTML = titleTxt;
  // document.getElementById('lblDescription').innerHTML = descriptionTxt;

  let listElement = document.getElementById('listElement');
  followersFollowed.forEach(json => {
    // 1. Create an item for follower
    let listItem = document.createElement('li');
    listItem.classList.add('result');
    // 2. Add the item text
    const name = json.name;
    const username = json.username;
    listItem.innerHTML = `${name} (@${username})`;
    // 3. Add listItem to the listElement
    listElement.appendChild(listItem);
  })
}

/*--Functions--*/
async function submitForm(e, form) {
    // 1. Prevent reloading page
    e.preventDefault();
    // 2. Submit the form
    // 2.1 User Interaction
    const btnSubmit = document.getElementById('btnSubmit');
    btnSubmit.disabled = true;
    setTimeout(() => btnSubmit.disabled = false, 2000);
    // 2.2 Build JSON body
    const jsonFormData = buildJsonFormData(form);
    // 2.3 Build Headers
    const headers = buildHeaders();
    // 2.4 Request & Response
    const response = await fetchService.performPostHttpRequest(`https://drrhop28ba.execute-api.us-east-1.amazonaws.com/dev/`, headers, jsonFormData);
    // 2.5 Encode response
    const responseEncoding = encodeURIComponent(JSON.stringify(response));
    // 2.6 Inform user of result
    if(response)
        window.location = `/success.html?res=${responseEncoding}`;
    else
        alert(`An error occured.`);
}

function buildHeaders(authorization = null) {
    const headers = {
        "Content-Type": "application/json",
        "Authorization": (authorization) ? authorization : "Bearer TOKEN_MISSING"
    };
    return headers;
}

function buildJsonFormData(form) {
    const jsonFormData = { };
    for(const pair of new FormData(form)) {
        jsonFormData[pair[0]] = pair[1];
    }
    return jsonFormData;
}
/*--/Functions--*/

/*--Event Listeners--*/
const sampleForm = document.querySelector("#sampleForm");
if(sampleForm) {
    sampleForm.addEventListener("submit", function(e) {
        submitForm(e, this);
    });
}
/*--/Event Listeners--*/
