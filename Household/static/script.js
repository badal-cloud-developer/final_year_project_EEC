
    function toggleMenu() {
      document.querySelector('.sidebar').classList.toggle('active');
    }

    function showSection(sectionId) {
      document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
      document.getElementById(sectionId).classList.add('active');
      document.querySelectorAll('.sidebar ul li').forEach(li => li.classList.remove('active'));
      const index = ['report','illegal','profile','notifications','mapSection'].indexOf(sectionId);
      document.querySelectorAll('.sidebar ul li')[index].classList.add('active');
      document.querySelector('.sidebar').classList.remove('active'); // collapse on mobile
    }

    

    // MAP INIT (OPTIONAL)
    
 