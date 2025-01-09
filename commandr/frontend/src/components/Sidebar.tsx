import { Settings } from '../types';

interface SidebarProps {
  settings: Settings;
  onSettingsChange: (settings: Settings) => void;
}

export default function Sidebar({ settings, onSettingsChange }: SidebarProps) {
  const handleTemperatureChange = (value: string) => {
    onSettingsChange({
      ...settings,
      temperature: parseFloat(value)
    });
  };

  const handleStreamToggle = () => {
    onSettingsChange({
      ...settings,
      streamEnabled: !settings.streamEnabled
    });
  };

  return (
    <div className="w-64 bg-gray-800 p-4 flex flex-col">
      <h1 className="text-xl font-bold text-white mb-8">CommandR</h1>
      
      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Temperature: {settings.temperature}
          </label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={settings.temperature}
            onChange={(e) => handleTemperatureChange(e.target.value)}
            className="w-full"
          />
        </div>

        <div>
          <label className="flex items-center space-x-2 text-gray-300">
            <input
              type="checkbox"
              checked={settings.streamEnabled}
              onChange={handleStreamToggle}
              className="form-checkbox h-4 w-4"
            />
            <span>Stream Response</span>
          </label>
        </div>
      </div>
    </div>
  );
}

