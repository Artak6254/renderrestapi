document.addEventListener("DOMContentLoaded", function () {

  // CSRF helper
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // First fetch for directions
  fetch("/api/flight_direction/grouped/")
    .then(response => {
      if (!response.ok) {
        throw new Error("Failed to fetch flight directions");
      }
      return response.json();
    })
    .then(data => {
      const fromSelect = document.getElementById("from_to");
      const toSelect = document.getElementById("to_there");

      fromSelect.innerHTML = '<option value="">Select</option>';
      toSelect.innerHTML = '<option value="">Select</option>';

      data.from_here.forEach(item => {
        const option = document.createElement("option");
        option.value = item.from_here;
        option.textContent = `${item.from_here} (${item.flight_airport_short_name})`;
        fromSelect.appendChild(option);
      });

      data.to_there.forEach(item => {
        const option = document.createElement("option");
        option.value = item.to_there;
        option.textContent = `${item.to_there} (${item.arrival_airport_short_name})`;
        toSelect.appendChild(option);
      });
    })
    .catch(error => console.error("❌ Error fetching flight directions:", error));

  // Add click event listener to search button
  const searchBtn = document.getElementById("flightSearchForm");
  if (!searchBtn) {
    console.error("❌ No element with id 'searchBtn' found");
    return;
  }

});




document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("flightSearchForm");
  const passengerFormContainer = document.getElementById("passengerFormContainer");

  if (!form) {
    console.warn("Form with ID 'flightSearchForm' not found.");
    return;
  }

  // Ստեղծում ենք submit կոճակը բայց սկզբում թաքնված
  const submitBtn = document.createElement("button");
  submitBtn.type = "submit";
  submitBtn.textContent = "Ուղարկել";
  submitBtn.style.padding = "10px 20px";
  submitBtn.style.backgroundColor = "#007bff";
  submitBtn.style.color = "white";
  submitBtn.style.border = "none";
  submitBtn.style.borderRadius = "5px";
  submitBtn.style.cursor = "pointer";
  submitBtn.style.fontSize = "16px";
  submitBtn.style.marginTop = "20px";
  submitBtn.style.display = "none"; // սկզբում թաքնված

  // Ավելացնում ենք form-ի վերջում
  form.appendChild(submitBtn);

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/api/search-flights/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      renderResults(data);
      generatePassengerForm(data);
      submitBtn.style.display = "block"; // այստեղ արդեն երևում է
    })
    .catch(error => {
      console.error("Error:", error);
    });
  });

  function renderResults(data) {
    const resultsContainer = document.getElementById("results");
    resultsContainer.innerHTML = "";

    const message = document.createElement("p");
    message.textContent = data.message;
    resultsContainer.appendChild(message);

    const flexContainer = document.createElement("div");
    flexContainer.style.display = "flex";
    flexContainer.style.gap = "30px";

    const departureDiv = document.createElement("div");
    departureDiv.innerHTML = "<h2>Գնալու թռիչքներ</h2>";

    if (data.departure_flights.length === 0) {
      departureDiv.innerHTML += "<p>Չկան համապատասխան գնալու թռիչքներ:</p>";
    } else {
      data.departure_flights.forEach(flight => {
        const flightDiv = createFlightBlock(flight);
        departureDiv.appendChild(flightDiv);
      });
    }

    flexContainer.appendChild(departureDiv);

    const returnDiv = document.createElement("div");
    returnDiv.innerHTML = "<h2>Վերադարձի թռիչքներ</h2>";

    if (!data.return_flights || data.return_flights.length === 0) {
      returnDiv.innerHTML += "<p>Չկան համապատասխան վերադարձի թռիչքներ:</p>";
    } else {
      data.return_flights.forEach(flight => {
        const flightDiv = createFlightBlock(flight);
        returnDiv.appendChild(flightDiv);
      });
    }

    flexContainer.appendChild(returnDiv);
    resultsContainer.appendChild(flexContainer);
  }

  function createFlightBlock(flight) {
    const flightDiv = document.createElement("div");
    flightDiv.style.border = "1px solid #ccc";
    flightDiv.style.padding = "10px";
    flightDiv.style.marginBottom = "15px";
    flightDiv.style.borderRadius = "8px";
    flightDiv.style.backgroundColor = "#f9f9f9";
  
    flightDiv.innerHTML = `
      <h3>${flight.from_here} ➔ ${flight.to_there}</h3>
      <p>Մեկնում․ ${flight.departure_date} - ${flight.departure_time}</p>
      <p>Ժամանում․ ${flight.arrival_time}</p>
      <h4>Տոմսեր:</h4>
      <ul style="padding-left: 20px;">
        ${flight.tickets.map(ticket => `
          <li>Տոմսի համար․ ${ticket.ticket_number} | Տիպ․ ${ticket.passenger_type} | Գին․ ${ticket.price} դրամ</li>
        `).join("")}
      </ul>
    `;

    // Ստեղծում ենք նստատեղերի բլոկը
    const seatsContainer = document.createElement("div");
    seatsContainer.style.marginTop = "15px";
    seatsContainer.innerHTML = "<h4>Նստատեղեր:</h4>";

    // Ավելացնում ենք բեռնելու կոճակ
    const loadSeatsBtn = document.createElement("button");
    loadSeatsBtn.textContent = "Բեռնել նստատեղերը";
    loadSeatsBtn.style.padding = "8px 16px";
    loadSeatsBtn.style.backgroundColor = "#007bff";
    loadSeatsBtn.style.color = "white";
    loadSeatsBtn.style.border = "none";
    loadSeatsBtn.style.borderRadius = "5px";
    loadSeatsBtn.style.cursor = "pointer";
    loadSeatsBtn.style.marginBottom = "10px";

    loadSeatsBtn.addEventListener("click", () => {
        loadSeats(flight.id, seatsContainer);
        loadSeatsBtn.style.display = "none";
    });

    seatsContainer.appendChild(loadSeatsBtn);
    flightDiv.appendChild(seatsContainer);

    return flightDiv;
}

function loadSeats(flightId, container) {
    fetch(`/api/flights_seats/?flight_id=${flightId}`)
        .then(response => response.json())
        .then(seats => {
            renderSeats(seats, container);
        })
        .catch(error => {
            console.error('Սխալ:', error);
            container.innerHTML += `<p style="color:red;">Չհաջողվեց բեռնել նստատեղերը։</p>`;
        });
}

function renderSeats(seats, container) {
    const seatsList = document.createElement("div");
    seatsList.style.display = "flex";
    seatsList.style.flexWrap = "wrap";
    seatsList.style.gap = "10px";

    seats.forEach(seat => {
        const seatDiv = document.createElement('div');
        seatDiv.style.border = '1px solid #ccc';
        seatDiv.style.padding = '10px';
        seatDiv.style.borderRadius = '8px';
        seatDiv.style.width = '150px';
        seatDiv.style.fontFamily = 'Arial, sans-serif';
        seatDiv.style.textAlign = 'center';
        seatDiv.style.backgroundColor = seat.is_taken ? '#ffcfcf' : '#ccffcc';

        const seatNumber = document.createElement('h4');
        seatNumber.textContent = `№ ${seat.seat_number}`;

        const seatType = document.createElement('p');
        seatType.textContent = `Տիպ․ ${seat.seat_type}`;

        const seatStatus = document.createElement('p');
        seatStatus.textContent = seat.is_taken ? 'Զբաղված' : 'Ազատ';

        seatDiv.appendChild(seatNumber);
        seatDiv.appendChild(seatType);
        seatDiv.appendChild(seatStatus);

        if (!seat.is_taken) {
            const selectBtn = document.createElement('button');
            selectBtn.textContent = 'Ընտրել';
            selectBtn.style.padding = '6px 12px';
            selectBtn.style.backgroundColor = '#28a745';
            selectBtn.style.color = 'white';
            selectBtn.style.border = 'none';
            selectBtn.style.borderRadius = '5px';
            selectBtn.style.cursor = 'pointer';
            selectBtn.style.marginTop = '5px';

            selectBtn.addEventListener('click', () => {
                alert(`Ընտրված է նստատեղը № ${seat.seat_number}`);
                // Այստեղ կարող ես հետագայում ավելացնել ընտրության պահպանում
            });

            seatDiv.appendChild(selectBtn);
        }

        seatsList.appendChild(seatDiv);
    });

    container.appendChild(seatsList);
}

  

  function generatePassengerForm(data) {
    passengerFormContainer.innerHTML = "<h3>Ուղևորների տվյալների մուտքագրում</h3>";
    passengerFormContainer.style.padding = "20px";
    passengerFormContainer.style.border = "1px solid #ccc";
    passengerFormContainer.style.borderRadius = "8px";
    passengerFormContainer.style.backgroundColor = "#fff";

    let allTickets = [];

    data.departure_flights.forEach(flight => {
      allTickets = allTickets.concat(flight.tickets);
    });

    if (data.return_flights) {
      data.return_flights.forEach(flight => {
        allTickets = allTickets.concat(flight.tickets);
      });
    }

    allTickets.forEach((ticket, index) => {
      const passengerDiv = document.createElement("div");
      passengerDiv.style.border = "1px solid #ddd";
      passengerDiv.style.padding = "15px";
      passengerDiv.style.marginBottom = "20px";
      passengerDiv.style.borderRadius = "8px";

      passengerDiv.innerHTML = `<h4>Ուղևոր ${index + 1} (${ticket.passenger_type})</h4>`;

      passengerDiv.appendChild(createInputField(`passengers[${index}][title]`, "Title", "text", true));
      passengerDiv.appendChild(createInputField(`passengers[${index}][full_name]`, "Full Name", "text", true));
      passengerDiv.appendChild(createInputField(`passengers[${index}][date_of_birth]`, "Date of Birth", "date", true));
      passengerDiv.appendChild(createInputField(`passengers[${index}][citizenship]`, "Citizenship", "text", true));
      passengerDiv.appendChild(createInputField(`passengers[${index}][passport_serial]`, "Passport Serial", "text", true));
      passengerDiv.appendChild(createInputField(`passengers[${index}][passport_validity_period]`, "Passport Validity", "date", true));

      // Միայն adults-ի համար ավելացնում ենք հեռախոս և email
      if (ticket.passenger_type === "adult") {
        passengerDiv.appendChild(createInputField(`passengers[${index}][phone]`, "Phone", "tel", true));
        passengerDiv.appendChild(createInputField(`passengers[${index}][email]`, "Email", "email", true));
      }


      // Hidden fields
      passengerDiv.innerHTML += `
        <input type="hidden" name="passengers[${index}][ticket_id]" value="${ticket.id}">
        <input type="hidden" name="passengers[${index}][passenger_type]" value="${ticket.passenger_type}">
        <input type="hidden" name="passengers[${index}][price]" value="${ticket.price}">
      `;

      passengerFormContainer.appendChild(passengerDiv);
    });
  }

  function createInputField(name, label, type, required = false, defaultValue = '') {
    const wrapper = document.createElement("div");
    wrapper.style.marginBottom = "12px";

    const labelEl = document.createElement("label");
    labelEl.textContent = label;
    labelEl.style.display = "block";
    labelEl.style.fontWeight = "600";
    labelEl.style.marginBottom = "4px";

    const inputEl = document.createElement("input");
    inputEl.type = type;
    inputEl.name = name;
    inputEl.value = defaultValue;
    inputEl.style.width = "100%";
    inputEl.style.padding = "8px";
    inputEl.style.border = "1px solid #ccc";
    inputEl.style.borderRadius = "5px";
    inputEl.style.fontSize = "14px";

    if (required) {
      inputEl.required = true;
    }

    wrapper.appendChild(labelEl);
    wrapper.appendChild(inputEl);
    return wrapper;
  }
});
