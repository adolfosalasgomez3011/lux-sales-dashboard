-- Enable UUID usage (optional, but good practice, though we use SERIAL/INTEGER here to match existing)
-- For this migration, we will stick to SERIAL/INTEGER IDs to minimize code changes in the app logic that expects integers.

-- Table 1: Businesses
CREATE TABLE public.businesses (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    tipo_negocio TEXT NOT NULL,
    direccion TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(nombre, direccion)
);

-- Table 2: Visits
CREATE TABLE public.visitas (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES public.businesses(id),
    fecha DATE NOT NULL,
    semana TEXT NOT NULL,
    notas TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 3: Opportunities
CREATE TABLE public.oportunidades (
    id SERIAL PRIMARY KEY,
    business_id INTEGER NOT NULL REFERENCES public.businesses(id),
    visita_id INTEGER REFERENCES public.visitas(id),
    fecha_contacto DATE NOT NULL,
    semana TEXT NOT NULL,
    m2_estimado INTEGER,
    producto_interes TEXT,
    siguiente_accion TEXT,
    estado TEXT DEFAULT 'Activa',
    source TEXT, -- Added column
    nombre_contacto TEXT, -- Added column
    cargo_contacto TEXT, -- Added column
    celular_contacto TEXT, -- Added column
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table 4: Sales
CREATE TABLE public.ventas (
    id SERIAL PRIMARY KEY,
    venta_id TEXT UNIQUE NOT NULL,
    business_id INTEGER NOT NULL REFERENCES public.businesses(id),
    oportunidad_id INTEGER REFERENCES public.oportunidades(id),
    fecha_cierre DATE NOT NULL,
    semana TEXT NOT NULL,
    m2_real INTEGER NOT NULL,
    producto TEXT NOT NULL,
    monto_soles DECIMAL(10,2) NOT NULL,
    fecha_instalacion DATE,
    estado TEXT DEFAULT 'Cerrada',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security (RLS)
-- For a simple internal tool, we might enable RLS but allow all operations for authenticated users (or anon if just using API key).
-- For now, enabling read/write for everyone with the API key.
ALTER TABLE public.businesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.visitas ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.oportunidades ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ventas ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Enable all access for anon/authenticated" ON public.businesses FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for anon/authenticated" ON public.visitas FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for anon/authenticated" ON public.oportunidades FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for anon/authenticated" ON public.ventas FOR ALL USING (true) WITH CHECK (true);
