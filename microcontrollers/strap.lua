local GRAVITY = {0, -10, 0}

local random_offset = property.getBool("Random Offset")

local sin, cos = math.sin, math.cos

local function dot(a, b) return a[1]*b[1] + a[2]*b[2] + a[3]*b[3] end

local function cross(a, b)
	return {
		a[2]*b[3] - a[3]*b[2],
		a[3]*b[1] - a[1]*b[3],
		a[1]*b[2] - a[2]*b[1]
	}
end

local function add(a, b)
	return {a[1] + b[1], a[2] + b[2], a[3] + b[3]}
end

local function sub(a, b)
	return {a[1] - b[1], a[2] - b[2], a[3] - b[3]}
end

local function mul(a, s)
	return {a[1]*s, a[2]*s, a[3]*s}
end

local function norm(v)
	return math.sqrt(dot(v, v))
end

local function normalize(v)
	return mul(v, 1 / norm(v))
end

local function mat3_mul_vec3(M, v)
	return {
		M[1]*v[1] + M[2]*v[2] + M[3]*v[3],
		M[4]*v[1] + M[5]*v[2] + M[6]*v[3],
		M[7]*v[1] + M[8]*v[2] + M[9]*v[3]
	}
end

local function mat3T_mul_vec3(M, v)
	return {
		M[1]*v[1] + M[4]*v[2] + M[7]*v[3],
		M[2]*v[1] + M[5]*v[2] + M[8]*v[3],
		M[3]*v[1] + M[6]*v[2] + M[9]*v[3]
	}
end

function apparent_gravity(R, v_local, omega_local, a_local)
	local omega_world = mat3_mul_vec3(R, omega_local)
	local a_world = mat3_mul_vec3(R, a_local)

	local a_inertial = a_world

	local w2 = dot(omega_world, omega_world)
	if w2 > 1e-10 then
		local v_world = mat3_mul_vec3(R, v_local)
		local r_world = mul(cross(omega_world, v_world), -1/w2)
		local a_centrifugal = cross(omega_world, cross(omega_world, r_world))
		a_inertial = add(a_inertial, a_centrifugal)
	end

	return mat3T_mul_vec3(R, sub(GRAVITY, a_inertial))
end

local function rodrigues(axis, s)
	if dot(axis, axis) < 1e-10 then
		return {
			1, 0, 0,
			0, 1, 0,
			0, 0, 1,
		}
	end
	axis = normalize(axis)

	local c = math.sqrt(1 - s*s)
	local one_c = 1 - c
	local ux, uy, uz = axis[1], axis[2], axis[3]

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
		r00, r01, r02,
		r10, r11, r12,
		r20, r21, r22,
	}
end

local function rotation_from_to(from, to)
	local axis = cross(normalize(to), normalize(from))
	return rodrigues(axis, norm(axis))
end

local function simulate_pendulum(dir, omega, g, k, d, dt)
	local axis = cross(dir, normalize(g))
	local alpha = add(mul(axis, k), mul(omega, -d))
	local omega_new = add(omega, mul(alpha, dt))
	local omega2 = dot(omega_new, omega_new)
	local dir_new = mat3_mul_vec3(rodrigues(omega, math.sin(math.sqrt(omega2) * dt)), dir)

	return dir_new, omega_new
end

local v_local = {0, 0, 0}
local p_omega = {0, 0, 0}
local p_dir = {0, -1, 0}

local gN = input.getNumber

function onTick()
	local euler_x, euler_y, euler_z = gN(4), gN(5), gN(6)
	local sx, cx = sin(euler_x), cos(euler_x)
	local sy, cy = sin(euler_y), cos(euler_y)
	local sz, cz = sin(euler_z), cos(euler_z)
	local R = {
		cy*cz, sx*sy*cz - cx*sz, cx*sy*cz + sx*sz,
		cy*sz, sx*sy*sz + cx*cz, cx*sy*sz - sx*cz,
		-sy, sx*cy, cx*cy
	}

	local v_local_new = {gN(7), gN(8), gN(9)}
	local a_local = mul(sub(v_local_new, v_local), 60)
	v_local = v_local_new

	local omega_local = {gN(10), gN(11), gN(12)}

	local g = apparent_gravity(R, v_local, omega_local, a_local)
	p_dir, p_omega = simulate_pendulum(p_dir, p_omega, g, 25, 2, 1/60)

	local mat3 = rotation_from_to({0, -1, 0}, p_dir)

	for i = 1, 9 do
		output.setNumber(i, mat3[i])
	end
	output.setBool(1, random_offset)
end
