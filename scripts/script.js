let keywords = [];
let cacheDate = '';
let currentPage = 1;
const pageSize = 20;

async function fetch_keywords() {
    try {
        const response = await fetch('/keywords');
        if (response.ok) {
            res = await response.json();
            keywords = res.data;
            cacheDate = new Date(res.cache_datetime);

            // Sort the keywords by length (trigrams, bigrams, and then unigrams)
            keywords.sort((a, b) => {
                const aLength = a[0].split(' ').length;
                const bLength = b[0].split(' ').length;
                return bLength - aLength;
            });

            display_keywords();
        } else {
            console.error('Failed to fetch keywords:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching keywords:', error);
    }
    finally {
        // Hide the progress spinner icon and show the refresh icon
        const refreshIcon = document.getElementById('refresh-icon');
        refreshIcon.className = 'fa-solid fa-rotate-right';

        // Restore the opacity of the table header
        const tableHeader = document.querySelector('#keywords_table thead');
        tableHeader.style.opacity = '1';
    }
}

function display_keywords() {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const currentPageKeywords = keywords.slice(startIndex, endIndex);

    const tbody = document.getElementById('keywords_tbody');
    tbody.innerHTML = '';

    display_pagination();
    currentPageKeywords.forEach(keyword_data => {
        const tr = document.createElement('tr');

        // Keyword and Current Month Count
        for (let i = 0; i < 2; i++) {
            const td = document.createElement('td');
            td.innerText = keyword_data[i];
            tr.appendChild(td);
        }

        // Calculate the previous month count
        const change = keyword_data[2];
        const previous_count = keyword_data[1] - change;

        // Add the previous month count cell
        const previousMonthCountCell = document.createElement('td');
        previousMonthCountCell.innerText = previous_count;
        tr.appendChild(previousMonthCountCell);

        // Calculate the percentage change
        const percentage_change = (previous_count === 0) ? "N/A" : (change * 100 / previous_count).toFixed(2) + '%';

        // Add the percentage change cell
        const percentageChangeCell = document.createElement('td');
        percentageChangeCell.innerText = percentage_change;
        if (percentage_change !== "N/A") {
            percentageChangeCell.style.color = change >= 0 ? 'green' : 'red';
        }
        tr.appendChild(percentageChangeCell);

        // Add the URLs cell
        const urlsCell = document.createElement('td');
        const postIdLinks = keyword_data[3].map(url => {
            const urlSearchParams = new URLSearchParams(url.split('?')[1]);
            const postId = urlSearchParams.get('t');
            return `<a href="${url}" target="_blank">${postId}</a>`;
        }).join(', '); // Separate the links with commas

        urlsCell.innerHTML = `
            <div class="urls-container">
                <button class="urls-toggle" onclick="toggleUrls(event)">
                    <i class="fa-solid fa-chevron-down"></i>
                </button>
                <div class="urls-content" style="display: none;">${postIdLinks}</div>
            </div>
        `;
        tr.appendChild(urlsCell);

        tbody.appendChild(tr);
    });

    display_pagination();
};

function toggleUrls(event) {
    const button = event.target.closest('.urls-toggle');
    const icon = button.querySelector('i');
    const urlsContent = button.nextElementSibling;

    if (urlsContent.style.display === 'none') {
        urlsContent.style.display = 'block';
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    } else {
        urlsContent.style.display = 'none';
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    }
}

function display_pagination() {
    const totalPages = Math.ceil(keywords.length / pageSize);

    // A helper function to create a pagination button
    function createPaginationButton(i) {
        const button = document.createElement('button');
        button.innerText = i;
        button.onclick = function () {
            currentPage = i;
            display_keywords();
        };

        if (i === currentPage) {
            button.classList.add('active');
        }

        return button;
    }

    // Populate the top and bottom pagination containers
    const paginationTopContainer = document.getElementById('pagination_top_container');
    const paginationBottomContainer = document.getElementById('pagination_bottom');
    paginationTopContainer.innerHTML = '';
    paginationBottomContainer.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const buttonTop = createPaginationButton(i);
        const buttonBottom = createPaginationButton(i);
        paginationTopContainer.appendChild(buttonTop);
        paginationBottomContainer.appendChild(buttonBottom);
    }
}

const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove the active class from all tabs and tab contents
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(tc => tc.classList.remove('active'));
        // Add the active class to the clicked tab and corresponding tab content
        tab.classList.add('active');
        document.querySelector(`#${tab.dataset.tab}`).classList.add('active');
    });
});

async function refresh_keywords() {
    // Show the progress spinner icon
    const refreshIcon = document.getElementById('refresh-icon');
    refreshIcon.className = 'fa-solid fa-spinner fa-spin';

    // Fade the table header white slightly
    const tableHeader = document.querySelector('#keywords_table thead');
    tableHeader.classList.add('table-header-loading');

    await fetch_keywords();

    // Update the last refresh timestamp
    const lastRefreshElement = document.getElementById('last_refresh');
    const timestamp = cacheDate.toLocaleString();
    lastRefreshElement.innerText = 'Updated on ' + timestamp;
}

window.onload = refresh_keywords;
