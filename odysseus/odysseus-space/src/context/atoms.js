import { atom } from 'jotai';

export const divisionsAtom = atom([]);
export const connectionsAtom = atom([]);
export const selectedPlanetAtom = atom(null);
export const connectionModeAtom = atom(false);
export const tooltipAtom = atom(null);
export const isDraggingAtom = atom(false);
export const visualSettingsAtom = atom({
  showLabels: true,
  connectionOpacity: 0.8,
  planetSize: 1,
  glowIntensity: 1.5,
});

export const connectionTypes = {
  hierarchy: {
    color: '#ff9966',
    width: 3,
    dash: false,
    glow: true,
  },
  collaboration: {
    color: '#66ffff',
    width: 2,
    dash: true,
    glow: false,
  },
  information: {
    color: '#9966ff',
    width: 1,
    dash: true,
    glow: false,
  },
};
