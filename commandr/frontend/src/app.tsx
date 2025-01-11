import { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import './style.css';

interface Settings {
    temperature: number;
    streamEnabled: boolean;
}

function App() {
    const [settings, setSettings] = useState<Settings>({
        temperature: 0.7,
        streamEnabled: true
    });

    return (
        <div className="flex h-screen bg-gray-900">
            <Sidebar settings={settings} onSettingsChange={setSettings} />
            <ChatWindow settings={settings} />
        </div>
    )
}

export default App