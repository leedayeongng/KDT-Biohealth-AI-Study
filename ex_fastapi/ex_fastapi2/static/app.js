// 로직은 01_spa와 완전히 같지만 요소 선택 방식(클래스 등)을 Tailwind에 맞게 일부 UI 렌더링 코드를 수정했습니다.
const apiUrl = '/items/';
let isEditing = false;

document.addEventListener('DOMContentLoaded', fetchItems);

async function fetchItems() {
    try {
        const response = await fetch(apiUrl);
        const items = await response.json();
        renderItems(items);
    } catch (error) {
        console.error('아이템 조회 에러:', error);
    }
}

// 👉 Tailwind CSS 클래스가 적용된 HTML로 동적 생성
function renderItems(items) {
    const listDiv = document.getElementById('item-list');
    listDiv.innerHTML = '';

    if (items.length === 0) {
        // Tailwind 컬러 유틸리티 (text-gray-500)
        listDiv.innerHTML = '<p class="text-gray-500 italic mt-4 text-center">등록된 아이템이 없습니다.</p>';
        return;
    }

    items.forEach(item => {
        const itemDiv = document.createElement('div');
        // 기존: 'item' 클래스 -> Tailwind: flex, border, p, rounded 등 유틸리티 클래스의 나열
        itemDiv.className = 'flex flex-col sm:flex-row justify-between items-center bg-white border border-gray-200 p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 mb-3';

        const descText = item.description ? `<span class="text-xs ml-2 text-gray-400">| ${item.description}</span>` : '';

        itemDiv.innerHTML = `
            <div class="flex flex-col mb-3 sm:mb-0">
                <span class="font-bold text-lg text-blue-600">
                    <span class="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded mr-2">ID: ${item.id}</span>
                    ${item.name}
                </span>
                <span class="text-sm text-gray-600 mt-1">가격: <span class="font-semibold text-gray-800">${item.price.toLocaleString()} 원</span> ${descText}</span>
            </div>
            <div class="flex space-x-2">
                <!-- Tailwind 기반 버튼 디자인 (Green) -->
                <button class="px-3 py-1.5 bg-green-500 text-white text-sm rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 transition-colors"
                    onclick="editItem(${item.id}, '${item.name}', '${item.description || ''}', ${item.price})">
                    수정
                </button>
                <!-- Tailwind 기반 버튼 디자인 (Red) -->
                <button class="px-3 py-1.5 bg-red-500 text-white text-sm rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 transition-colors"
                    onclick="deleteItem(${item.id})">
                    삭제
                </button>
            </div>
        `;
        listDiv.appendChild(itemDiv);
    });
}

async function submitForm() {
    const idInput = document.getElementById('item-id');
    const nameInput = document.getElementById('item-name');
    const descInput = document.getElementById('item-desc');
    const priceInput = document.getElementById('item-price');

    const id = parseInt(idInput.value);
    const name = nameInput.value.trim();
    const desc = descInput.value.trim();
    const price = parseFloat(priceInput.value);

    if (isNaN(id) || !name || isNaN(price)) {
        alert("ID, 이름, 가격은 필수 항목입니다.");
        return;
    }

    const payload = { id, name, description: desc || null, price };

    try {
        const method = isEditing ? 'PUT' : 'POST';
        const url = isEditing ? `${apiUrl}${id}` : apiUrl;

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            resetForm();
            fetchItems();
        } else {
            const errorData = await response.json();
            alert("Error: " + errorData.detail);
        }
    } catch (error) {
        console.error('요청 에러:', error);
    }
}

async function deleteItem(id) {
    if (!confirm(`정말 ID ${id} 아이템을 삭제하시겠습니까?`)) return;
    try {
        const response = await fetch(`${apiUrl}${id}`, { method: 'DELETE' });
        if (response.ok) {
            fetchItems();
        } else {
            const errorData = await response.json();
            alert("삭제 실패: " + (errorData.detail || "오류"));
        }
    } catch (error) {
        console.error('삭제 에러:', error);
    }
}

function editItem(id, name, desc, price) {
    document.getElementById('item-id').value = id;
    document.getElementById('item-id').disabled = true; // ID 변경 불가 (Tailwind 폼에서 disabled 디자인도 적용됨)
    document.getElementById('item-name').value = name;
    document.getElementById('item-desc').value = desc;
    document.getElementById('item-price').value = price;

    document.getElementById('submit-btn').innerText = "아이템 수정";
    document.getElementById('form-title').innerText = "아이템 수정 모드";
    document.getElementById('cancel-btn').classList.remove("hidden"); // Tailwind 기반 보이기

    isEditing = true;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function resetForm() {
    document.getElementById('item-id').value = '';
    document.getElementById('item-id').disabled = false;
    document.getElementById('item-name').value = '';
    document.getElementById('item-desc').value = '';
    document.getElementById('item-price').value = '';

    document.getElementById('submit-btn').innerText = "아이템 추가";
    document.getElementById('form-title').innerText = "새 아이템 추가";
    document.getElementById('cancel-btn').classList.add("hidden"); // Tailwind 기반 숨기기

    isEditing = false;
}
