// Define the API URL
const apiUrl = _config.api.invokeUrl
const decodeUrl = _config.api.decodeURL

// Get the id token from the URL after sign in
function getIdTokenFromUrl() {
    const urlParams = new URLSearchParams(window.location.hash.replace('#', '?'));
    return urlParams.get('id_token');
}

const idToken = getIdTokenFromUrl();
console.log("idToken: ")
console.log(idToken)

// Global variable to store the email
let user_email = null;

// API call to the decodeToken Lambda, sends id token and receives the user email
function fetchAndStoreEmail(decodeUrl, accessToken) {
    const urlWithToken = `${decodeUrl}?token=${encodeURIComponent(accessToken)}`;
    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    };

    fetch(urlWithToken, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched data:", data);
            // Assuming the API returns a JSON object with an 'email' field
            if (data.email) {
                console.log(`Email: ${data.email}`);
                // Optionally, do something with the email, like storing it
                user_email = data.email
                fetchEmployees()
            }
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}


fetchAndStoreEmail(decodeUrl, idToken);

// Get employees that match the user's email
async function fetchEmployees() {
    // Combine API url with user email param
    const urlWithEmail = `${apiUrl}?email=${encodeURIComponent(user_email)}`;

    // GET request
    try {
        const response = await fetch(urlWithEmail, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': idToken
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log("data: ", data);
        const data_list = JSON.parse(data.body);
        console.log("list data: ", data_list);
        const tableBody = document.getElementById('employees');
        
        tableBody.innerHTML = '';

        data_list.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="px-4 py-2">${item.name}</td>
                <td class="px-4 py-2">${item.email}</td>
                <td class="px-4 py-2">${item.title}</td>
                <td class="px-4 py-2">${item.wage}</td>
                <td class="px-4 py-2">${item.supervisor}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}
  
// Add a new employee
async function addEmployee() {
    // Gather input values
    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;
    let title = document.getElementById('title').value;
    let wage = document.getElementById('wage').value;
    let supervisor = document.getElementById('supervisor').value;

    // Construct the employee object
    let employee = { name, email, title, wage, supervisor, user_email };
    console.log('Post body: ', JSON.stringify(employee));

    // Make a POST request API
    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify(employee),
    })
    .then(response => response.json())
    .then(data => {
        // Handle response data
        console.log(data);
        // Reload the employees list to include the new employee
        fetchEmployees();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
