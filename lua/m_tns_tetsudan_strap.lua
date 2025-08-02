function norm(v)
    return math.sqrt(v[1]*v[1] + v[2]*v[2] + v[3]*v[3])
end

function normalize(v)
    local n = norm(v)
    return {v[1] / n, v[2] / n, v[3] / n}
end

function cross(a, b)
    return {
        a[2]*b[3] - a[3]*b[2],
        a[1]*b[3] - a[3]*b[1],
        a[1]*b[2] - a[2]*b[1]
    }
end

function rotation_from_to(a, b)
    local axis = cross(normalize(a), normalize(b))
    local ax, ay, az = axis[1], axis[2], axis[3]
    local s = norm({ax, ay, az})

    if s < 1e-8 then
        return matrix.identity()
    end

    local c = math.sqrt(1 - s*s)
    --local theta = math.asin(s)
    --local c = math.cos(theta)
    local one_c = 1 - c

    local ux, uy, uz = ax / s, ay / s, az / s

    -- Rodrigues' rotation formula
    local r00 = c + ux*ux*one_c
    local r01 = ux*uy*one_c - uz*s
    local r02 = ux*uz*one_c + uy*s
    local r10 = uy*ux*one_c + uz*s
    local r11 = c + uy*uy*one_c
    local r12 = uy*uz*one_c - ux*s
    local r20 = uz*ux*one_c - uy*s
    local r21 = uz*uy*one_c + ux*s
    local r22 = c + uz*uz*one_c

    return {
        r00, r01, r02, 0,
        r10, r11, r12, 0,
        r20, r21, r22, 0,
        0, 0, 0, 1
    }
end

local ax, az = 0, 0

function onTick(tick_time)
    local composite, success = component.getInputLogicSlotComposite(0)
    if success then
        ax = composite.float_values[1]
        az = composite.float_values[2]
    end
end

function onRender()
    component.renderMesh0(rotation_from_to({0, -1, 0}, {-ax, -1, -az}))
end
