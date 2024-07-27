function editEvent(id) {
    let element = document.querySelector('.event[data-event="' + id + '"]');
    let event = {
        'id': id,
        'year': element.dataset.year,
        'month': element.dataset.month,
        'day': element.dataset.day,
        'name': element.querySelector('[data-field="name"]').textContent,
        'url': '',
        'parent_name': '',
        'parent_url': ''
    }
    if (element.querySelector('[data-field="url"]')) {
        event.url = element.querySelector('[data-field="url"]').getAttribute('href');
    }
    if (element.querySelector('[data-field="parent"]')) {
        event.parent_name = element.querySelector('[data-field="parent"]').textContent;
        event.parent_url = element.querySelector('[data-field="parent"]').getAttribute('href');
    }
    console.log(event);
    let modalElement = document.querySelector('#addItemModal');
    const modal = new bootstrap.Modal(modalElement, {});
    document.getElementById('id').value = event.id;
    document.getElementById('year').value = event.year;
    document.getElementById('month').value = event.month;
    document.getElementById('day').value = event.day;
    document.getElementById('name').value = event.name;
    document.getElementById('url').value = event.url;
    document.getElementById('parent_name').value = event.parent_name;
    document.getElementById('parent_url').value = event.parent_url;
    modal.show();
}

function newEvent() {
    const modal = new bootstrap.Modal('#addItemModal', {});
    document.getElementById('id').value = '';
    document.getElementById('year').value = '';
    document.getElementById('month').value = current_month;
    document.getElementById('day').value = current_day;
    document.getElementById('name').value = '';
    document.getElementById('url').value = '';
    document.getElementById('parent_name').value = '';
    document.getElementById('parent_url').value = '';
    modal.show();
}