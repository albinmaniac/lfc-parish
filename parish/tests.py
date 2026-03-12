from django.test import TestCase

# Create your tests here.

<style>
  *, *::before, *::after { 
    margin: 0; 
    padding: 0; 
    box-sizing: border-box; 
  }

  .logo {
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: rise 1.2s cubic-bezier(.16,1,.3,1) both;
  }

  @keyframes rise {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .img-wrap {
    position: relative;
    width: 280px;
    height: 280px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .img-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: radial-gradient(circle,
      rgba(255,210,40,0.35) 0%,
      rgba(255,180,0,0.08) 50%,
      transparent 72%);
    animation: halo 3.5s ease-in-out infinite;
  }

  @keyframes halo {
    0%,100% { opacity: 0.7; transform: scale(1); }
    50%     { opacity: 1; transform: scale(1.05); }
  }

  .img-wrap img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
    position: relative;
    z-index: 1;
    filter: drop-shadow(0 8px 32px rgba(180,130,0,0.4));
  }
</style>

<div class="logo">
  <div class="img-wrap">
    <img src="{% static 'images/logo.png' %}" alt="Church Logo">
  </div>
</div>