import stars from '../assets/stars.png'
import constellations from '../assets/constellations.png'
import khamsas from '../assets/khamsas.png'
import mandalas from '../assets/mandalas.png'

export default function Background() {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden" style={{ zIndex: 0 }}>
      {/* Stars full background */}
      <img
        src={stars}
        alt=""
        className="absolute inset-0 w-full h-full object-cover"
        style={{ opacity: 0.15 }}
      />

      {/* Mandalas — top left */}
      <img src={mandalas} alt=""
        className="absolute top-0 left-0 w-[480px]"
        style={{ opacity: 0.22, transform: 'translate(-20%, -20%)' }}
      />

      {/* Mandalas — bottom right */}
      <img src={mandalas} alt=""
        className="absolute bottom-0 right-0 w-[420px]"
        style={{ opacity: 0.20, transform: 'translate(20%, 25%) rotate(180deg)' }}
      />

      {/* Constellations — top right */}
      <img src={constellations} alt=""
        className="absolute top-0 right-0 w-[400px]"
        style={{ opacity: 0.22, transform: 'translate(10%, -10%) rotate(10deg)' }}
      />

      {/* Constellations — bottom left */}
      <img src={constellations} alt=""
        className="absolute bottom-0 left-0 w-[360px]"
        style={{ opacity: 0.18, transform: 'translate(-10%, 15%) rotate(-10deg)' }}
      />

      {/* Khamsas — bottom left */}
      <img src={khamsas} alt=""
        className="absolute bottom-0 left-0 w-[400px]"
        style={{ opacity: 0.20, transform: 'translate(-15%, 20%)' }}
      />

      {/* Khamsas — top right, flipped */}
      <img src={khamsas} alt=""
        className="absolute top-0 right-0 w-[360px]"
        style={{ opacity: 0.18, transform: 'translate(15%, -20%) scaleY(-1)' }}
      />

      {/* Constellations — mid left */}
      <img src={constellations} alt=""
        className="absolute top-1/2 left-0 w-[300px]"
        style={{ opacity: 0.15, transform: 'translate(-20%, -50%) rotate(-5deg)' }}
      />

      {/* Constellations — mid right */}
      <img src={constellations} alt=""
        className="absolute top-1/2 right-0 w-[300px]"
        style={{ opacity: 0.15, transform: 'translate(20%, -50%) rotate(5deg)' }}
      />

      {/* Stars cluster — bottom center */}
      <img src={stars} alt=""
        className="absolute bottom-0 left-1/2 w-[500px]"
        style={{ opacity: 0.14, transform: 'translateX(-50%)' }}
      />
    </div>
  )
}
