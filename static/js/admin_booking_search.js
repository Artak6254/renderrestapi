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
  submitBtn.style.display = "none";
  form.appendChild(submitBtn);

  let selectedSeats = {};
  let baseTotalPrice = 0;
  let allTickets = {};
  let allSeats = [];
  let manualSeats = []; 
  let searchResultData = null;
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
        searchResultData = data;
        renderResults(data);
        generatePassengerForm(data);
        submitBtn.style.display = "block";
      })
      .catch(error => console.error("Error:", error));
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
        const flightDiv = createFlightBlock(flight, "departure");
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
        const flightDiv = createFlightBlock(flight, "return");
        returnDiv.appendChild(flightDiv);
      });
    }

    flexContainer.appendChild(returnDiv);
    resultsContainer.appendChild(flexContainer);
  }

  function createFlightBlock(flight, type) {
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
    <h4>Նստատեղեր:</h4>
    <ul style="padding-left: 20px;">
      ${flight.flight_seats.map(seat => `
        <li>
          ${seat.seat_number}
          <input type="checkbox" class="seat-checkbox" data-seat-id="${seat.id}" ${seat.is_taken ? "checked disabled" : ""}>
        </li>
      `).join("")}
    </ul>
  `;
  setTimeout(() => {
    document.querySelectorAll(".seat-checkbox").forEach(checkbox => {
      checkbox.addEventListener("change", async function () {
        const seatId = this.dataset.seatId;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (this.checked) {
          const response = await fetch(`/api/flights_seats/${seatId}/set_taken/`, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken }
          });
          if (response.ok) {
            alert(`Նստատեղը ամրագրվեց`);
            this.disabled = true;

            // ✅ Ավելացնում ենք նստատեղը manualSeats array-ի մեջ
            const seatNumberText = this.closest('li').textContent.trim().split("\n")[0].trim();
            manualSeats.push({
              seat_id: parseInt(seatId),
              seat_number: seatNumberText,
              seat_type: type,
              is_taken: true,
              flight_id: flight.id
            });
          } else {
            alert("Սխալ առաջացավ");
            this.checked = false;
          }
        }
      });
    });
  }, 0);
  

    const seatsContainer = document.createElement("div");
    seatsContainer.style.marginTop = "15px";
    seatsContainer.innerHTML = "<h4>Նստատեղերի ընտրություն:</h4>";

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
      loadSeats(flight.id, seatsContainer, flight.tickets, type);
      loadSeatsBtn.style.display = "none";
    });

    seatsContainer.appendChild(loadSeatsBtn);
    flightDiv.appendChild(seatsContainer);
    return flightDiv;
  }

  function loadSeats(flightId, container, tickets, type) {
    fetch(`/api/flights_seats/?flight_id=${flightId}`)
      .then(response => response.json())
      .then(seats => {
        allSeats = allSeats.concat(seats.map(seat => ({...seat, flight_id: flightId, type: type})));
        renderSeats(seats, container, tickets, type);
      })
      .catch(error => {
        console.error('Սխալ:', error);
        container.innerHTML += `<p style="color:red;">Չհաջողվեց բեռնել նստատեղերը։</p>`;
      });
  }

  function renderSeats(seats, container, tickets, type) {
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
      seatDiv.style.transition = 'border-color 0.3s ease';
    
      const seatNumber = document.createElement('h4');
      seatNumber.textContent = `№ ${seat.seat_number}`;
      seatDiv.appendChild(seatNumber);
    
      if (seat.is_taken) {
        seatDiv.style.backgroundColor = '#ffcfcf';
        seatDiv.appendChild(document.createTextNode("Զբաղված"));
      } else {
        seatDiv.style.backgroundColor = '#ccffcc';
    
        tickets.forEach(ticket => {
          if (ticket.passenger_type === 'baby') {
            return; // baby-ի համար նստատեղ չընտրենք
          }
          const selectBtn = document.createElement('button');
          selectBtn.textContent = `Ընտրել ${ticket.passenger_type}`;
    
          // Կոճակի սթայլ
          Object.assign(selectBtn.style, {
            marginTop: '5px',
            padding: '8px 16px',
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontWeight: '600',
            transition: 'background-color 0.3s ease',
          });
    
          // Մկնիկի վրա անցնելիս գույնի փոփոխություն
          selectBtn.addEventListener('mouseenter', () => {
            selectBtn.style.backgroundColor = '#0056b3';
          });
          selectBtn.addEventListener('mouseleave', () => {
            selectBtn.style.backgroundColor = '#007bff';
          });
    
          selectBtn.addEventListener('click', () => {
            // Նախ մաքրենք բոլոր մյուս նստատեղերի border-ը նույն տիպի և տոմսի համար
            const previouslySelected = document.querySelectorAll(`div[data-ticket="${type}_${ticket.id}"]`);
            previouslySelected.forEach(div => {
              div.style.border = '1px solid #ccc';
            });
    
            selectedSeats[`${type}_${ticket.id}`] = seat.id;
    
            // Այս նստատեղի border-ը դարձնենք գույնը
            seatDiv.style.border = '3px solid #ff9800';
    
            alert(`${ticket.passenger_type} համար ընտրված է ${type} նստատեղ № ${seat.seat_number}`);
            calculateTotalPrice();
          });
    
          // Տեղադրում ենք data-ticket, որպեսզի մաքրման ժամանակ գտնենք
          seatDiv.setAttribute('data-ticket', `${type}_${ticket.id}`);
    
          seatDiv.appendChild(selectBtn);
        });
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

    allTickets = {};

    const departureFlights = data.departure_flights || [];

    // Ընդամենը վերցնում ենք departure_flights առաջին թռիչքից տոմսերը
    let firstFlight = departureFlights.length > 0 ? departureFlights[0] : null;

    if (!firstFlight) {
        alert("Չկան թռիչքներ");
        return;
    }

    let tickets = firstFlight.tickets;

    tickets.forEach((ticket, index) => {
        allTickets[ticket.id] = ticket;
        const passengerDiv = createPassengerForm(index + 1, ticket);
        passengerFormContainer.appendChild(passengerDiv);
    });

    baseTotalPrice = Object.values(allTickets).reduce((sum, t) => sum + parseInt(t.price), 0);
    calculateTotalPrice();
}

function createPassengerForm(index, ticket) {
  const passengerDiv = document.createElement("div");
  passengerDiv.style.border = "1px solid #ddd";
  passengerDiv.style.padding = "15px";
  passengerDiv.style.marginBottom = "20px";
  passengerDiv.style.borderRadius = "8px";

  passengerDiv.innerHTML = `<h4>Ուղևոր ${index} (${ticket.passenger_type})</h4>`;
  passengerDiv.appendChild(createInputField(`title_${ticket.id}`, "Title", "text", true));
  passengerDiv.appendChild(createInputField(`full_name_${ticket.id}`, "Full Name", "text", true));
  passengerDiv.appendChild(createInputField(`date_of_birth_${ticket.id}`, "Date of Birth", "date", true));
  passengerDiv.appendChild(createInputField(`citizenship_${ticket.id}`, "Citizenship", "text", true));
  passengerDiv.appendChild(createInputField(`passport_serial_${ticket.id}`, "Passport Serial", "text", true));
  passengerDiv.appendChild(createInputField(`passport_validity_${ticket.id}`, "Passport Validity", "date", true));
  if (ticket.passenger_type === "adult") {
    passengerDiv.appendChild(createInputField(`phone_${ticket.id}`, "Phone", "tel", true));
    passengerDiv.appendChild(createInputField(`email_${ticket.id}`, "Email", "email", true));
  }
  return passengerDiv;
}

  function createInputField(name, label, type, required = false) {
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
    inputEl.style.width = "100%";
    inputEl.style.padding = "8px";
    inputEl.style.border = "1px solid #ccc";
    inputEl.style.borderRadius = "5px";
    inputEl.style.fontSize = "14px";
    if (required) inputEl.required = true;
    wrapper.appendChild(labelEl);
    wrapper.appendChild(inputEl);
    return wrapper;
  }

  function calculateTotalPrice() {
    const extraPrice = Object.keys(selectedSeats).length * 2000;
    const total = baseTotalPrice + extraPrice;
    let totalPriceDiv = document.getElementById("totalPrice");
    if (!totalPriceDiv) {
      totalPriceDiv = document.createElement("div");
      totalPriceDiv.id = "totalPrice";
      totalPriceDiv.style.fontWeight = "bold";
      totalPriceDiv.style.fontSize = "18px";
      totalPriceDiv.style.marginTop = "20px";
      passengerFormContainer.appendChild(totalPriceDiv);
    }
    totalPriceDiv.textContent = `Ընդհանուր Գումարը․ ${total} դրամ`;
  }
  submitBtn.addEventListener("click", async function (e) {
    e.preventDefault();
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
    const passengers_data = [];
    const ticket_data = [];
    const seats = [];  // Ապագայում կուղարկվի archive-ին
  
    let totalPassengers = 0;
    let totalPrice = 0;
  
    const passengerTypePrices = {
      adult: 20000,
      child: 10000,
      baby: 5000,
    };
  
    const passengerTypesSet = new Set();
  
    // ✅ 1. Վերլուծում ենք բոլոր տոմսերը
    for (let ticketId in allTickets) {
      const ticket = allTickets[ticketId];
      totalPassengers += 1;
      totalPrice += parseInt(ticket.price);
  
      // ✅ Ուղևորի տվյալները
      const passenger = {
        ticket_id: ticketId,
        title: document.querySelector(`[name=title_${ticketId}]`).value,
        full_name: document.querySelector(`[name=full_name_${ticketId}]`).value,
        date_of_birth: document.querySelector(`[name=date_of_birth_${ticketId}]`).value,
        citizenship: document.querySelector(`[name=citizenship_${ticketId}]`).value,
        passport_serial: document.querySelector(`[name=passport_serial_${ticketId}]`).value,
        passport_validity: document.querySelector(`[name=passport_validity_${ticketId}]`).value,
        phone: ticket.passenger_type === "adult" ? document.querySelector(`[name=phone_${ticketId}]`).value : null,
        email: ticket.passenger_type === "adult" ? document.querySelector(`[name=email_${ticketId}]`).value : null,
        passenger_type: ticket.passenger_type,
      };
  
      passengers_data.push(passenger);
      passengerTypesSet.add(ticket.passenger_type);
      console.log(selectedSeats, allSeats);
      // ✅ Նստատեղերը (departure/return) ավելացնել seats մեջ
      ["departure", "return"].forEach(type => {
        const seatId = selectedSeats[`${type}_${ticketId}`];
        if (seatId) {
          const foundSeat = allSeats.find(s => s.id === seatId);
          if (foundSeat) {
            seats.push({
              seat_id: foundSeat.id,
              seat_number: foundSeat.seat_number,
              seat_type: type,
              is_taken: true,
              flight_id: foundSeat.flight_id,
            });
          }
        }
      });
      
    }
  
    // ✅ 2. Ստեղծում ենք ticket_data
    for (let ticketId in allTickets) {
      const ticket = allTickets[ticketId];
      ticket_data.push({
        ticket_id: ticketId,
        ticket_number: ticket.ticket_number,
        ticket_type: ticket.ticket_type,
        price: ticket.price,
        ticket_is_sold: true,
      });
    }
  
    // ✅ 3. Թռիչքի տվյալները
    const departureFlight = searchResultData.departure_flights?.[0] || null;
    const returnFlight = searchResultData.return_flights?.[0] || null;
  
    if (!departureFlight) {
      alert("Չհաջողվեց գտնել գնալու թռիչքի տվյալները։");
      return;
    }
  
    const archiveData = {
      flight_from: departureFlight.from_here,
      flight_to: departureFlight.to_there,
      flight_departure_date: departureFlight.departure_date,
      flight_return_date: returnFlight ? returnFlight.departure_date : null,
      departure_time: departureFlight.departure_time,
      arrival_time: departureFlight.arrival_time,
      total_passengers: totalPassengers,
      total_price: totalPrice.toString(),
      passengers_data: passengers_data,
      ticket_data: ticket_data,
      seats: [...seats, ...manualSeats], 
    };
  
    console.log("📦 Արխիվացվող տվյալները:", archiveData);
  
    // ✅ 4. Ուղարկում ենք արխիվ
    submitBtn.disabled = true;
    submitBtn.innerText = "Արխիվացվում է...";
  
    try {
      const response = await fetch("http://localhost:8085/api/sold_archive/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(archiveData),
      });
  
      if (!response.ok) {
        const errorText = await response.text();
        console.error("❌ Արխիվացման սխալ:", errorText);
        alert("Սխալ առաջացավ տվյալները ուղարկելիս։");
      } else {
        alert("Բոլոր տվյալները հաջողությամբ արխիվացվեցին։");
        // location.reload();
      }
    } catch (error) {
      console.error("❌ Ցանցային սխալ:", error);
      alert("Ցանցային սխալ առաջացավ։");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerText = "Ուղարկել";
    }
  });
  
  
  

});

