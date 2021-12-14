import FetchService from './service/FetchService';

/*-- Objects --*/
const fetchService = new FetchService();
/*-- /Objects --*/

/*-- On Load -- */
if (window.location.href.includes('success.html')) {
  const queryString = window.location.search;
  const encodedResponse = queryString.split("?res=")[1];
  const decodedResponse = decodeURIComponent(encodedResponse);
  const responseJSON = JSON.parse(decodedResponse);
  console.log(responseJSON);

  const sourceName = responseJSON.source.name;
  const targetName = responseJSON.target.name;
  const followersFollowed = Array.from(responseJSON.followers_followed);
  const count = followersFollowed.length;

  var titleTxt;
  if (count > 0) {
    titleTxt = `${targetName} follows ${count} accounts that follow ${sourceName}`;
  } else {
    titleTxt = `${targetName} does not follow anyone that follows ${sourceName}`;
  }
  document.getElementById('lblTitle').innerHTML = titleTxt;
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
