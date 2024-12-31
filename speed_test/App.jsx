import { useState, useEffect, useRef } from 'react';
import { Moon, Sun } from 'lucide-react';

const SpeedGauge = () => {
  const websocketRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem('darkMode') === 'true';
  });
  const [speed, setSpeed] = useState(0);
  const [maxSpeed, setMaxSpeed] = useState(100);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [finalSpeed, setFinalSpeed] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  const radius = 120;
  const strokeWidth = 20;
  const center = radius + strokeWidth;
  const circumference = 2 * Math.PI * radius;
  const maxAngle = 270;

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  const connectWebSocket = () => {
    if (websocketRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket('ws://localhost:8000/ws/speedtest');
    websocketRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
      setError(null);
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
      setConnectionStatus('disconnected');
      reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setError('Connection error. Retrying...');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Received data:', data);

        switch (data.type) {
          case 'speed_update':
            setSpeed(data.speed);
            setMaxSpeed((prev) => Math.max(prev, Math.ceil(data.speed / 100) * 100));
            break;

          case 'test_complete':
            setFinalSpeed(data.current_speed);
            setIsLoading(false);
            break;

          case 'error':
            setError(data.message);
            setIsLoading(false);
            break;

          default:
            console.log('Unknown message type:', data.type);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  };

  useEffect(() => {
    connectWebSocket();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, []);

  const startSpeedTest = () => {
    if (connectionStatus !== 'connected') {
      setError('Not connected to server. Reconnecting...');
      connectWebSocket();
      return;
    }

    setIsLoading(true);
    setError(null);
    setSpeed(0);
    setFinalSpeed(null);

    websocketRef.current.send('start_test');
  };

  const getStrokeDashoffset = (value) => {
    const progress = Math.min(value / maxSpeed, 1);
    return circumference - (progress * (circumference * (maxAngle / 360)));
  };

  const getSpeedColor = (speed) => {
    if (speed < maxSpeed * 0.3) return darkMode ? '#4ade80' : '#22c55e';
    if (speed < maxSpeed * 0.6) return darkMode ? '#facc15' : '#eab308';
    return darkMode ? '#f87171' : '#ef4444';
  };

  return (
    <div className="min-h-screen w-full transition-colors duration-200 dark:bg-gray-900 bg-gray-50">
      <div className="absolute top-4 right-4">
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-lg transition-colors duration-200 dark:bg-gray-800 dark:text-yellow-400 bg-gray-200 text-gray-800"
        >
          {darkMode ? <Sun size={24} /> : <Moon size={24} />}
        </button>
      </div>

      <div className="flex flex-col items-center justify-center min-h-screen p-8">
        <div className={`mb-4 text-sm ${
          connectionStatus === 'connected'
            ? 'text-green-600 dark:text-green-400'
            : 'text-red-600 dark:text-red-400'
        }`}>
          {connectionStatus === 'connected' ? 'Connected to server' : 'Connecting...'}
        </div>

        {error && (
          <div className="mb-4 text-red-600 dark:text-red-400">
            {error}
          </div>
        )}

        <div className="relative">
          <svg
            width={center * 2}
            height={center * 2}
            className="transform -rotate-90"
          >
            <circle
              cx={center}
              cy={center}
              r={radius}
              fill="none"
              className="stroke-gray-200 dark:stroke-gray-700"
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={circumference * ((360 - maxAngle) / 360)}
              strokeLinecap="round"
            />
            <circle
              cx={center}
              cy={center}
              r={radius}
              fill="none"
              stroke={getSpeedColor(speed)}
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={getStrokeDashoffset(speed)}
              strokeLinecap="round"
              className="transition-all duration-200"
            />
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-900 dark:text-white">
            <div className="text-4xl font-bold">
              {finalSpeed !== null ? finalSpeed.toFixed(1) : speed.toFixed(1)}
            </div>
            <div className="text-xl">Mbps</div>
            <div className="text-sm mt-2 text-gray-500 dark:text-gray-400">
              {finalSpeed !== null ? 'Current Speed' : 'Current Speed'}
            </div>
          </div>
        </div>

        <button
          onClick={startSpeedTest}
          disabled={isLoading || connectionStatus !== 'connected'}
          className={`mt-8 px-6 py-2 rounded-lg text-white font-medium transition-colors
            ${isLoading
              ? 'bg-gray-400 dark:bg-gray-600 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700'
            }`}
        >
          {isLoading ? 'Testing...' : 'Start Speed Test'}
        </button>
      </div>
    </div>
  );
};

function App() {

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <SpeedGauge />
    </div>
  )
}

export default App
